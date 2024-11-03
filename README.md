# Text-to-Video Generator

A Python script that converts text into video with speech. It creates a video with customizable background color and text overlay, along with computer-generated speech narration. You can also use your own video as a background.

## Features

- Converts text to speech using Google's Text-to-Speech (gTTS)
- Creates video with customizable background and text styling
- Supports centered or custom text positioning
- Automatically synchronizes video duration with speech
- Supports custom video backgrounds with automatic looping/trimming
- Text overlay with semi-transparent background for better visibility

## Installation

Clone the repository and install the required packages:

```bash
git clone <repository-url>
cd <repository-name>
pip install -r requirements.txt
```

Or install required packages manually:

```bash
pip install moviepy pillow numpy gtts
```

## Usage

Basic usage:

```python
from main import create_video_from_text

create_video_from_text("Hello! This is a test video.")
```

Advanced usage with custom styling:

```python
create_video_from_text(
    text="Your text here",
    output_filename="custom_output.mp4",
    bg_color=(25, 25, 112),  # Midnight Blue
    text_color='yellow',
    text_size=40,
    text_position='center'
)
```

Using a background video:

```python
create_video_from_text(
    text="Your text here",
    output_filename="video_background.mp4",
    text_color='white',
    text_size=40,
    background_video="path_to_your_video.mp4"
)
```

## Parameters

- `text` (str): The text to convert into video
- `output_filename` (str, optional): Output video filename. Default: "output.mp4"
- `duration` (float, optional): Video duration in seconds. If None, matches audio duration
- `bg_color` (tuple, optional): Background color in RGB. Default: (0, 0, 0) (black)
- `text_color` (str, optional): Text color. Default: 'white'
- `text_size` (int, optional): Font size. Default: 30
- `text_position` (str/tuple, optional): Text position. Can be 'center' or (x, y) coordinates. Default: 'center'
- `background_video` (str, optional): Path to a video file to use as background. If provided, bg_color is ignored

## Generated Files

The script generates:
- An MP4 video file (specified by output_filename)
- A temporary audio file that is automatically cleaned up

## Notes

- Uses PIL for text rendering
- Requires an internet connection for text-to-speech conversion
- When using a background video:
  - If the video is shorter than the audio, it will loop automatically
  - If the video is longer than the audio, it will be trimmed
  - Text is overlaid with semi-transparent background for better visibility
- Default video resolution is 640x480 pixels when not using a background video
- When using a background video, output resolution matches the background video resolution
