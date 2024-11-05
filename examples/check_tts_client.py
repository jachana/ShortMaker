from elevenlabs.text_to_speech import client
print("Available attributes in elevenlabs.text_to_speech.client module:")
for attr in dir(client):
    if not attr.startswith('_'):
        print(f"- {attr}")
