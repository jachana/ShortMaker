import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, VideoFileClip, VideoClip
from .tts_providers import TTSProvider, GTTSProvider
import os

def create_frame(text, size=(640, 480), bg_color=(0, 0, 0), text_color='white', 
                text_size=30, text_position='center'):
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
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate text position
    if text_position == 'center':
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
    elif isinstance(text_position, tuple):
        x, y = text_position
    
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Convert PIL image to numpy array
    return np.array(img)

def create_video_from_text(text, output_filename="output.mp4", duration=None, 
                         bg_color=(0, 0, 0), text_color='white', 
                         text_size=30, text_position='center',
                         background_video=None, tts_provider: TTSProvider = None):
    # Use default GTTSProvider if none specified
    if tts_provider is None:
        tts_provider = GTTSProvider()
    
    # Generate speech using the provided TTS provider
    temp_audio_path = "temp_audio.mp3"
    tts_provider.generate_speech(text, temp_audio_path)
    
    # Load the audio to get its duration
    audio = AudioFileClip(temp_audio_path)
    
    # If duration not specified, use audio duration
    if duration is None:
        duration = audio.duration

    if background_video:
        # Normalize path and check if file exists
        background_video = os.path.normpath(background_video)
        if not os.path.exists(background_video):
            raise FileNotFoundError(f"Background video not found: {background_video}")
        video = VideoFileClip(background_video)
        
        # Loop the video if it's shorter than the audio
        if video.duration < duration:
            video = video.loop(duration=duration)
        # Trim the video if it's longer than the audio
        else:
            video = video.subclip(0, duration)
        
        # Create a frame with the text
        text_frame = create_frame(text, size=video.size, text_color=text_color, 
                                text_size=text_size, text_position=text_position)
        
        # Create a function to overlay text on video frames
        def combine_frame(get_frame, t):
            video_frame = get_frame(t)
            # Create a semi-transparent overlay for better text visibility
            overlay = np.zeros_like(video_frame)
            overlay[text_frame > 0] = text_frame[text_frame > 0]
            return video_frame * 0.7 + overlay * 0.3  # Adjust blend factors as needed
        
        # Create the final video with text overlay
        final_video = VideoClip(lambda t: combine_frame(video.get_frame, t), 
                              duration=duration)
    else:
        # Create a frame with the text (original functionality)
        frame = create_frame(text, bg_color=bg_color, text_color=text_color, 
                            text_size=text_size, text_position=text_position)
        
        def make_frame(t):
            return frame
        
        final_video = VideoClip(make_frame, duration=duration)
    
    # Add audio to video
    final_video = final_video.set_audio(audio)
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    audio.close()
    final_video.close()
    if background_video:
        video.close()
    
    # Remove temporary audio file
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

# Example usage
if __name__ == "__main__":
    sample_text = "Hello! This is a test video with a background video."
    
    # Example with default gTTS
    create_video_from_text(
        sample_text,
        output_filename="output_default.mp4",
        text_color='white',
        text_size=40
    )
    
    # Example with ElevenLabs
    from .tts_providers import ElevenLabsProvider
    eleven_labs_provider = ElevenLabsProvider(
        api_key="your-api-key",
        voice_id="your-voice-id"
    )
    create_video_from_text(
        sample_text,
        output_filename="output_elevenlabs.mp4",
        text_color='white',
        text_size=40,
        tts_provider=eleven_labs_provider
    )
    
    # Example with OpenAI
    from .tts_providers import OpenAITTSProvider
    openai_provider = OpenAITTSProvider(
        api_key="your-api-key",
        voice="alloy"
    )
    create_video_from_text(
        sample_text,
        output_filename="output_openai.mp4",
        text_color='white',
        text_size=40,
        tts_provider=openai_provider
    )
