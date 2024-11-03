# ShortMaker

A Python utility for creating short videos from text with optional background video support.

## Features

- Create videos from text with text-to-speech
- Support for background videos
- Customizable text appearance (size, color, position)
- Automatic video duration based on speech length
- Clean temporary file handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.main import create_video_from_text

# Basic usage
create_video_from_text(
    "Hello! This is a test video.",
    output_filename="output.mp4"
)

# With custom parameters
create_video_from_text(
    "Hello! This is a test video with background.",
    output_filename="output_with_background.mp4",
    text_color='white',
    text_size=40,
    background_video="background.mp4"
)
```

## Testing

The project includes a comprehensive test suite. To run the tests:

```bash
pytest tests/test_video_maker.py -v
```

Tests cover:
- Frame creation with default parameters
- Custom frame sizes
- Custom colors and text positions
- Video creation with and without background
- Error handling for invalid inputs

## Requirements

See `requirements.txt` for a full list of dependencies:
- moviepy>=1.0.3
- Pillow>=9.0.0
- numpy>=1.21.0
- gTTS>=2.3.1
- pytest>=7.0.0 (for testing)
