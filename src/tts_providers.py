from abc import ABC, abstractmethod
from gtts import gTTS
import requests
import openai
import os
import json

class TTSProvider(ABC):
    @abstractmethod
    def generate_speech(self, text: str, output_path: str) -> None:
        pass

class GTTSProvider(TTSProvider):
    def generate_speech(self, text: str, output_path: str) -> None:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)

class ElevenLabsProvider(TTSProvider):
    def __init__(self, 
                 api_key: str, 
                 voice_id: str = None,
                 model: str = "eleven_monolingual_v1",
                 stability: float = 0.5,
                 similarity_boost: float = 0.75):
        """
        Initialize ElevenLabs TTS provider with customizable parameters.
        
        Args:
            api_key: Your ElevenLabs API key
            voice_id: Voice ID to use (defaults to Rachel)
            model: Model to use for synthesis
            stability: Voice stability (0-1)
            similarity_boost: Similarity boost factor (0-1)
        """
        self.api_key = api_key
        self.voice_id = voice_id or "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        self.model = model
        self.stability = stability
        self.similarity_boost = similarity_boost

    def generate_speech(self, text: str, output_path: str) -> None:
        """
        Generate speech from text using ElevenLabs API.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
        """
        try:
            # API endpoint
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

            # Request headers
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }

            # Request body
            data = {
                "text": text,
                "model_id": self.model,
                "voice_settings": {
                    "stability": self.stability,
                    "similarity_boost": self.similarity_boost
                }
            }

            # Make the request
            response = requests.post(url, json=data, headers=headers)
            
            # Check if request was successful
            response.raise_for_status()
            
            # Save the audio directly to file
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
        except Exception as e:
            print(f"Error details: {str(e)}")
            raise

class OpenAITTSProvider(TTSProvider):
    def __init__(self, api_key: str, model: str = "tts-1", voice: str = "alloy"):
        self.api_key = api_key
        self.model = model
        self.voice = voice
        openai.api_key = api_key

    def generate_speech(self, text: str, output_path: str) -> None:
        response = openai.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
        )
        response.stream_to_file(output_path)
