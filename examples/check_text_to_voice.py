import elevenlabs.text_to_voice as ttv
print("Available attributes in elevenlabs.text_to_voice module:")
for attr in dir(ttv):
    if not attr.startswith('_'):
        print(f"- {attr}")
