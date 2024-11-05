import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, VideoFileClip, VideoClip, concatenate_videoclips
from src.tts_providers import TTSProvider, GTTSProvider
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def split_text_into_chunks(text, max_chunk_length=300, chunk_overlap=50):
    """
    Split long text into chunks with optional overlap.
    
    Args:
        text (str): The input text to be split
        max_chunk_length (int): Maximum length of each chunk
        chunk_overlap (int): Number of words to overlap between chunks
    
    Returns:
        list: A list of text chunks
    """
    # Remove extra whitespace and split into sentences
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for i, sentence in enumerate(sentences):
        # Check if adding this sentence would exceed max length
        sentence_length = len(sentence)
        
        # If current chunk would become too long, start a new chunk
        if current_length + sentence_length > max_chunk_length and current_chunk:
            # Join current chunk and add to chunks
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            
            # Start new chunk with this sentence
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # Log chunk information
    logger.info(f"Number of text chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks, 1):
        logger.info(f"Chunk {i}: {chunk}")
    
    return chunks

def create_frame(text, size=(640, 480), bg_color=(0, 0, 0), text_color='white', 
                text_size=30, text_position='center', fade_factor=1.0):
    """
    Create a video frame with text.
    Added fade_factor parameter for smooth transitions.
    """
    # Validate size parameter
    if not isinstance(size, tuple) or len(size) != 2 or size[0] <= 0 or size[1] <= 0:
        raise ValueError("Size must be a tuple of two positive integers")
        
    # Create a PIL Image with the background color
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use default font since it's available on all systems
    try:
        font = ImageFont.truetype("arial.ttf", text_size)
    except:
        font = ImageFont.load_default()
    
    # Dynamically adjust text size to fit the screen
    def get_wrapped_text(text, font, max_width):
        lines = []
        words = text.split()
        current_line = words[0]
        
        for word in words[1:]:
            # Check if adding the word would exceed max width
            test_line = current_line + " " + word
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = text_bbox[2] - text_bbox[0]
            
            if line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)
        return lines

    # Reduce text size until it fits
    while text_size > 10:
        font = ImageFont.truetype("arial.ttf", text_size)
        wrapped_text = get_wrapped_text(text, font, size[0] - 40)  # 40px padding
        
        # Calculate total text height
        text_lines = []
        for line in wrapped_text:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_lines.append(text_bbox)
        
        total_text_height = sum(line[3] - line[1] for line in text_lines)
        line_spacing = text_size // 4
        total_height = total_text_height + (len(wrapped_text) - 1) * line_spacing
        
        if total_height <= size[1] - 40:  # 40px padding
            break
        
        text_size -= 2
    
    # Calculate vertical position
    if text_position == 'center':
        y = (size[1] - total_height) // 2
    else:
        y = 20  # Default top padding
    
    # Draw wrapped text with fade effect
    for line in wrapped_text:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = text_bbox[2] - text_bbox[0]
        
        # Horizontal centering
        x = (size[0] - line_width) // 2
        
        # Apply fade effect to text color
        if isinstance(text_color, str):
            # Convert color name to RGB
            text_color_img = Image.new('RGB', (1, 1), text_color)
            text_color_rgb = text_color_img.getpixel((0, 0))
        else:
            text_color_rgb = text_color
            
        faded_color = tuple(int(c * fade_factor) for c in text_color_rgb)
        draw.text((x, y), line, font=font, fill=faded_color)
        y += text_bbox[3] - text_bbox[1] + line_spacing
    
    # Convert PIL image to numpy array
    return np.array(img)

def create_video_from_text(text, output_filename="output.mp4", duration=None, 
                         bg_color=(0, 0, 0), text_color='white', 
                         text_size=30, text_position='center',
                         background_video=None, tts_provider: TTSProvider = None,
                         max_chunk_length=300, chunk_overlap=50):
    """
    Create a video from text with synchronized audio and text display.
    """
    # Use default GTTSProvider if none specified
    if tts_provider is None:
        tts_provider = GTTSProvider()
    
    # Split text into chunks
    text_chunks = split_text_into_chunks(text, max_chunk_length, chunk_overlap)
    
    # Generate all audio chunks first and get their durations
    chunk_data = []
    for i, chunk in enumerate(text_chunks):
        temp_audio_path = f"temp_audio_chunk_{i}.mp3"
        tts_provider.generate_speech(chunk, temp_audio_path)
        audio = AudioFileClip(temp_audio_path)
        chunk_data.append({
            'text': chunk,
            'audio': audio,
            'duration': audio.duration,
            'audio_path': temp_audio_path
        })
    
    # Prepare video clips for each chunk
    video_clips = []
    
    for i, data in enumerate(chunk_data):
        chunk = data['text']
        audio = data['audio']
        chunk_duration = data['duration']
        
        # Create a function to generate frames with fade effects
        def make_frame_with_fade(t, chunk_text=chunk):
            # Calculate fade in/out factors
            fade_duration = min(0.5, chunk_duration / 4)  # 0.5 seconds or 1/4 of duration
            fade_in = min(t / fade_duration, 1) if t < fade_duration else 1
            fade_out = min((chunk_duration - t) / fade_duration, 1) if t > (chunk_duration - fade_duration) else 1
            fade_factor = min(fade_in, fade_out)
            
            if background_video:
                # Get background frame
                video_frame = background_video_clip.get_frame(t % background_video_clip.duration)
                
                # Create text frame with current fade factor
                text_frame = create_frame(chunk_text, size=(video_frame.shape[1], video_frame.shape[0]),
                                       text_color=text_color, text_size=text_size,
                                       text_position=text_position, fade_factor=fade_factor)
                
                # Blend frames
                return video_frame * 0.7 + text_frame * 0.3 * fade_factor
            else:
                # Create frame with solid background
                return create_frame(chunk_text, text_color=text_color, text_size=text_size,
                                 text_position=text_position, bg_color=bg_color,
                                 fade_factor=fade_factor)
        
        if background_video:
            # Load background video if not already loaded
            if 'background_video_clip' not in locals():
                background_video = os.path.normpath(background_video)
                if not os.path.exists(background_video):
                    raise FileNotFoundError(f"Background video not found: {background_video}")
                background_video_clip = VideoFileClip(background_video)
            
            # Loop or trim background video to match chunk duration
            if background_video_clip.duration < chunk_duration:
                background_video_clip = background_video_clip.loop(duration=chunk_duration)
            else:
                background_video_clip = background_video_clip.subclip(0, chunk_duration)
        
        # Create the video clip for this chunk
        chunk_video = VideoClip(lambda t: make_frame_with_fade(t), duration=chunk_duration)
        chunk_video = chunk_video.set_audio(audio)
        video_clips.append(chunk_video)
    
    # Concatenate all video clips
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    final_video.close()
    if background_video and 'background_video_clip' in locals():
        background_video_clip.close()
    
    for data in chunk_data:
        audio = data['audio']
        audio_path = data['audio_path']
        audio.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Example usage remains the same
if __name__ == "__main__":
    sample_text = "Hello! This is a test video with a background video. We are demonstrating text chunking functionality to break down long text into smaller, more manageable pieces that can be displayed sequentially during video generation."
    
    # Example with default gTTS
    create_video_from_text(
        sample_text,
        output_filename="output_chunked_default.mp4",
        text_color='white',
        text_size=40,
        max_chunk_length=100,  # Customize chunk length
        chunk_overlap=20       # Customize overlap between chunks
    )
