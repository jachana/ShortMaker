import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoClip
import os

def create_frame(text, size=(640, 480), bg_color=(0, 0, 0), text_color='white', 
                text_size=30, text_position='center'):
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
                         text_size=30, text_position='center'):
    # Create speech from text
    tts = gTTS(text=text, lang='en')
    tts.save("temp_audio.mp3")
    
    # Load the audio to get its duration
    audio = AudioFileClip("temp_audio.mp3")
    
    # If duration not specified, use audio duration
    if duration is None:
        duration = audio.duration
    
    # Create a frame with the text
    frame = create_frame(text, bg_color=bg_color, text_color=text_color, 
                        text_size=text_size, text_position=text_position)
    
    # Create video clip from the frame
    def make_frame(t):
        return frame
    
    video = VideoClip(make_frame, duration=duration)
    
    # Add audio to video
    final_video = video.set_audio(audio)
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    audio.close()
    final_video.close()
    
    # Remove temporary audio file
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

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
