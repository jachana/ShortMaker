import sys
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

try:
    from src.main import create_video_from_text
    from src.tts_providers import GTTSProvider

    # Long text to demonstrate chunking
    long_text = """
    Artificial Intelligence (AI) is transforming the world in unprecedented ways. 
    From healthcare to transportation, AI technologies are revolutionizing how we live and work. 
    Machine learning algorithms can now diagnose diseases, predict market trends, and even drive autonomous vehicles. 

    The potential of AI extends far beyond simple automation. It enables complex problem-solving, 
    data analysis, and decision-making processes that were once thought to be exclusively human domains. 
    Researchers are continuously pushing the boundaries of what AI can achieve, developing more sophisticated 
    neural networks and deep learning models.

    However, the rise of AI also brings important ethical considerations. Questions about privacy, 
    job displacement, and the potential misuse of powerful AI technologies are at the forefront of 
    global discussions. Balancing technological innovation with responsible development is crucial 
    for ensuring that AI benefits humanity as a whole.

    As we move forward, interdisciplinary collaboration will be key. Computer scientists, 
    ethicists, policymakers, and industry leaders must work together to create frameworks 
    that guide the responsible development and deployment of AI technologies.
    """

    # Use GTTSProvider explicitly
    gTTS_provider = GTTSProvider()

    # Generate a video with text chunking
    create_video_from_text(
        long_text, 
        output_filename="ai_explanation_video.mp4", 
        text_color='white', 
        text_size=30, 
        max_chunk_length=300,  # Adjust chunk length as needed
        chunk_overlap=50,      # Provide some context between chunks
        tts_provider=gTTS_provider
    )

    print("Video generation complete. Check 'ai_explanation_video.mp4'.")

except Exception as e:
    logger.error(f"Error during video generation: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)
