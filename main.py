from moviepy.config import change_settings
import os

# Configure MoviePy to use ImageMagick
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe')
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})

from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip

def create_video_from_text(text, output_filename="output.mp4", duration=None, 
                          bg_color=(0, 0, 0), text_color='white', 
                          text_size=30, text_position='center'):
    # Create speech from text
    tts = gTTS(text=text, lang='en')
    tts.save("temp_audio.mp3")
    
    # Load the audio to get its duration
    audio = AudioFileClip("temp_audio.mp3")
    
    # If duration not specified, use audio duration
    if duration is None:
        duration = audio.duration
    
    # Create background
    size = (640, 480)
    video = ColorClip(size, bg_color, duration=duration)
    
    # Create text overlay
    txt_clip = TextClip(text, fontsize=text_size, color=text_color)
    
    # Position the text
    if text_position == 'center':
        txt_clip = txt_clip.set_position('center').set_duration(duration)
    elif isinstance(text_position, tuple):
        txt_clip = txt_clip.set_position(text_position).set_duration(duration)
    
    # Combine background, text, and audio
    final_video = CompositeVideoClip([video, txt_clip])
    final_video = final_video.set_audio(audio)
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    audio.close()
    final_video.close()

# Example usage
if __name__ == "__main__":
    sample_text = "Hello! This is a test video created from text."
    
    # Example with custom styling
    create_video_from_text(
        sample_text,
        bg_color=(25, 25, 112),  # Midnight Blue
        text_color='yellow',
        text_size=40
    )
