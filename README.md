# ShortMaker

A Python utility for creating short videos from text with optional background video support.

## Features

- Create videos from text with text-to-speech
- Support for background videos
- Customizable text appearance (size, color, position)
- Automatic video duration based on speech length
- Clean temporary file handling
- Multiple TTS providers support (Google TTS, ElevenLabs, OpenAI)

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

### Using ElevenLabs TTS

```python
from src.tts_providers import ElevenLabsProvider

# Initialize with default settings
tts = ElevenLabsProvider(api_key="your-api-key")

# Initialize with custom settings
tts = ElevenLabsProvider(
    api_key="your-api-key",
    voice_id="custom-voice-id",  # Default is Rachel
    stability=0.7,               # Voice stability (0-1)
    similarity_boost=0.8,        # Similarity boost (0-1)
    style=0.5,                  # Speaking style influence (0-1)
    use_speaker_boost=True      # Enhance speaker clarity
)

# Generate speech
tts.generate_speech("Your text here", "output.mp3")
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
- elevenlabs>=0.5.0
- openai>=1.3.0
- pytest>=7.0.0 (for testing)

## TTS Providers

### ElevenLabs
The ElevenLabs provider offers high-quality, customizable text-to-speech with the following features:
- Multiple voice options
- Adjustable voice stability
- Similarity boost control
- Style control
- Speaker boost for enhanced clarity

### Google TTS
Basic text-to-speech functionality with multiple language support.

### OpenAI
High-quality text-to-speech using OpenAI's latest models with multiple voice options.
