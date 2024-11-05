import os
from src.tts_providers import ElevenLabsProvider

def test_elevenlabs_tts():
    # Get API key from environment variable
    api_key = os.getenv('ELVENLAB_API_KEY')
    if not api_key:
        raise ValueError("Please set ELVENLAB_API_KEY environment variable")

    # Initialize provider with default settings
    tts = ElevenLabsProvider(api_key=api_key)

    # Test text
    text = "Hello! This is a test of the ElevenLabs text to speech system."
    output_path = "tests/test_output.mp3"

    try:
        print("Generating speech...")
        # Generate speech
        tts.generate_speech(text, output_path)
        
        # Verify file exists and has content
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"Success! Generated audio file at {output_path}")
            print(f"File size: {size} bytes")
            return True
        else:
            print(f"Error: File {output_path} was not created")
            return False
    except Exception as e:
        print(f"Error during speech generation: {str(e)}")
        return False
    finally:
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
            print("Cleaned up test file")

if __name__ == "__main__":
    test_elevenlabs_tts()
