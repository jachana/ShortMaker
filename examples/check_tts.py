import elevenlabs.text_to_speech as tts
print("Available attributes in elevenlabs.text_to_speech module:")
for attr in dir(tts):
    if not attr.startswith('_'):
        print(f"- {attr}")
