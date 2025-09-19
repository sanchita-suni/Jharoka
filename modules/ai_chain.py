import io
import os
import requests
import base64
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
    Generates images based on a list of prompts using the Gemini API (imagen-3.0-generate-002 model).
    
    Args:
        prompts (list): A list of text prompts for image generation.
    
    Returns:
        list: A list of base64 data URLs for the generated images.
    """
    image_data_urls = []
    
    # You will need to replace this with a valid API key for the Gemini API.
    # It is recommended to use environment variables for this.
    # For this example, we'll use an empty string as a placeholder.
    api_key = os.getenv("GEMINI_API_KEY", "")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"

    if not api_key:
        print("GEMINI_API_KEY is not set. Returning mock images.")
        return [
            "https://placehold.co/400x400/007bff/ffffff?text=Mockup+1", 
            "https://placehold.co/400x400/ff6347/ffffff?text=Mockup+2"
        ]

    for prompt in prompts:
        payload = {
            "instances": {
                "prompt": prompt
            },
            "parameters": {
                "sampleCount": 1
            }
        }
        
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes
            
            result = response.json()
            
            if 'predictions' in result and len(result['predictions']) > 0 and 'bytesBase64Encoded' in result['predictions'][0]:
                base64_data = result['predictions'][0]['bytesBase64Encoded']
                image_data_urls.append(f"data:image/png;base64,{base64_data}")
            else:
                print(f"No image data found in response for prompt: {prompt}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during API call: {e}")
            image_data_urls.append(f"https://placehold.co/400x400/ff6347/ffffff?text=Error")
            
    return image_data_urls
