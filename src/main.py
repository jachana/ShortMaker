import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, VideoFileClip, VideoClip, concatenate_videoclips
from src.tts_providers import TTSProvider, GTTSProvider
import os

def split_text_into_chunks(text, max_chunk_length=100, overlap=20):
    """
    Split long text into chunks with optional overlap.
    
    Args:
        text (str): The input text to be split
        max_chunk_length (int): Maximum length of each chunk
        overlap (int): Number of words to overlap between chunks
    
    Returns:
        list: A list of text chunks
    """
    # Split text into words
    words = text.split()
    
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        
        # If current chunk exceeds max length, create a new chunk
        if len(' '.join(current_chunk)) > max_chunk_length:
            # Add the chunk (excluding the last few overlapping words)
            chunks.append(' '.join(current_chunk[:-overlap] if overlap > 0 else current_chunk))
            
            # Start next chunk with overlapping words
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def create_video_from_text(text, output_filename="output.mp4", duration=None, 
                         bg_color=(0, 0, 0), text_color='white', 
                         text_size=30, text_position='center',
                         background_video=None, tts_provider: TTSProvider = None,
                         max_chunk_length=100, chunk_overlap=20):
    # Use default GTTSProvider if none specified
    if tts_provider is None:
        tts_provider = GTTSProvider()
    
    # Split text into chunks
    text_chunks = split_text_into_chunks(text, max_chunk_length, chunk_overlap)
    
    # Prepare video clips for each chunk
    video_clips = []
    
    for chunk in text_chunks:
        # Generate speech for this chunk
        temp_audio_path = "temp_audio_chunk.mp3"
        tts_provider.generate_speech(chunk, temp_audio_path)
        
        # Load the audio to get its duration
        audio = AudioFileClip(temp_audio_path)
        chunk_duration = audio.duration
        
        if background_video:
            # Normalize path and check if file exists
            background_video = os.path.normpath(background_video)
            if not os.path.exists(background_video):
                raise FileNotFoundError(f"Background video not found: {background_video}")
            video = VideoFileClip(background_video)
            
            # Loop or trim the video to match chunk duration
            if video.duration < chunk_duration:
                video = video.loop(duration=chunk_duration)
            else:
                video = video.subclip(0, chunk_duration)
            
            # Create a frame with the text
            text_frame = create_frame(chunk, size=video.size, text_color=text_color, 
                                    text_size=text_size, text_position=text_position)
            
            # Create a function to overlay text on video frames
            def combine_frame(get_frame, t):
                video_frame = get_frame(t)
                # Create a semi-transparent overlay for better text visibility
                overlay = np.zeros_like(video_frame)
                overlay[text_frame > 0] = text_frame[text_frame > 0]
                return video_frame * 0.7 + overlay * 0.3  # Adjust blend factors as needed
            
            # Create the final video with text overlay
            chunk_video = VideoClip(lambda t: combine_frame(video.get_frame, t), 
                                  duration=chunk_duration)
        else:
            # Create a frame with the text (original functionality)
            frame = create_frame(chunk, bg_color=bg_color, text_color=text_color, 
                                text_size=text_size, text_position=text_position)
            
            def make_frame(t):
                return frame
            
            chunk_video = VideoClip(make_frame, duration=chunk_duration)
        
        # Add audio to video chunk
        chunk_video = chunk_video.set_audio(audio)
        video_clips.append(chunk_video)
        
        # Clean up
        audio.close()
        if background_video:
            video.close()
    
    # Concatenate all video chunks
    final_video = concatenate_videoclips(video_clips)
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    final_video.close()
    
    # Remove temporary audio files
    for chunk_file in os.listdir('.'):
        if chunk_file.startswith('temp_audio_chunk'):
            os.remove(chunk_file)

# Existing example usage remains the same
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
