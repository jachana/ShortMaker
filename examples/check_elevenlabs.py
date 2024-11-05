import elevenlabs
print("Available attributes in elevenlabs package:")
for attr in dir(elevenlabs):
    if not attr.startswith('_'):
        print(f"- {attr}")
