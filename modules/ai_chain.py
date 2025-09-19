import io
import os
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
