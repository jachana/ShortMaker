


from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, VideoFileClip

def create_video_from_text(text, output_filename="output.mp4", duration=None):
    # Create speech from text
    tts = gTTS(text=text, lang='en')
    tts.save("temp_audio.mp3")
    
    # Load the audio to get its duration
    audio = AudioFileClip("temp_audio.mp3")
    
    # If duration not specified, use audio duration
    if duration is None:
        duration = audio.duration
    
    # Create a simple black background
    size = (640, 480)
    bg_color = (0, 0, 0)
    video = ColorClip(size, bg_color, duration=duration)
    
    # Combine video with audio
    final_video = video.set_audio(audio)
    
    # Write the result
    final_video.write_videofile(output_filename, fps=24)
    
    # Clean up
    audio.close()
    final_video.close()

# Example usage
if __name__ == "__main__":
    sample_text = "Hello! This is a test video created from text."
    create_video_from_text(sample_text)
