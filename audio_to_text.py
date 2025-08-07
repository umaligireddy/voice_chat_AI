from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str) -> str:

    try:
        with open (file_path, "rb") as audio_file:
            transcript= client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
                )
            return transcript.text
    except Exception as e:
        print(f"An error occurred while transcribing the audio: {e}")
        return "Transcription failed."   
    