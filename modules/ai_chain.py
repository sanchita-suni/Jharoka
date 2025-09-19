import io
import os
import replicate
from google.cloud import speech

# --- IMPORTANT SETUP FOR GOOGLE CLOUD SPEECH-TO-TEXT API ---
# To use this code, you must first set up a Google Cloud project and
# enable the Speech-to-Text API.
# You also need to create a service account and download a JSON key file.
#
# The environment variable GOOGLE_APPLICATION_CREDENTIALS must be
# set to the path of your JSON key file.
#
# Example (run this in your terminal):
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
# -------------------------------------------------------------

# Replicate API configuration
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    print("Warning: REPLICATE_API_TOKEN not found. Image generation will use mock data.")

def transcribe_audio(audio_file_bytes: bytes) -> str:
    """
    Uses the Google Cloud Speech-to-Text API to transcribe audio bytes into text.

    Args:
        audio_file_bytes: The audio file as a bytes object.
        
    Returns:
        The transcribed text as a string.
    """
    # Instantiates a client for the Google Cloud Speech-to-Text API.
    client = speech.SpeechClient()

    # The audio file must be sent as a RecognitionAudio object.
    audio = speech.RecognitionAudio(content=audio_file_bytes)

    # The configuration tells the API how to process the audio.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, # or WAV, etc.
        language_code="en-US", # Change to the language you're using.
    )

    # Performs synchronous speech recognition.
    response = client.recognize(config=config, audio=audio)

    # Extracts the transcribed text from the response.
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + " "

    return transcribed_text.strip()

def generate_mockup_images(prompts: list) -> list:
    """
    Generates images based on a list of prompts using the Nano Banana (Replicate) API.
    If the API token is not set, it returns placeholder images.
    
    Args:
        prompts (list): A list of text prompts for image generation.
    
    Returns:
        list: A list of URLs for the generated images.
    """
    image_urls = []
    
    if not REPLICATE_API_TOKEN:
        print("REPLICATE_API_TOKEN is not set. Returning mock images.")
        return [
            "https://placehold.co/400x400/007bff/ffffff?text=Mockup+1", 
            "https://placehold.co/400x400/ff6347/ffffff?text=Mockup+2"
        ]

    try:
        for prompt in prompts:
            # Call the Replicate API for each prompt
            output = replicate.run(
                "ai-banana/banana:9b49b917614d9de2be91097e3766736a6e27c7f466b020054700d3369a838531",
                input={
                    "model_id": "sdxl",
                    "prompt": prompt,
                    "model_revision": "fp16",
                    "negative_prompt": "blurry, low quality, cartoon, anime",
                    "prior_num_inference_steps": 25,
                    "num_inference_steps": 50
                }
            )
            image_url = output[0] # Get the URL of the generated image
            image_urls.append(image_url)
            print(f"Generated image for prompt '{prompt}': {image_url}")
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        # Fallback to mock images if the API call fails
        image_urls = [
            "https://placehold.co/400x400/007bff/ffffff?text=Mockup+1", 
            "https://placehold.co/400x400/ff6347/ffffff?text=Mockup+2"
        ]
        
    return image_urls
