import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_audio(dialogue):
    """
    Generates audio from the given structured dialogue using OpenAI's TTS model.
    """
    audio_file_paths = []  # List to store paths of generated audio files
    try:
        for index, entry in enumerate(dialogue["dialogue"]):
            role = entry["role"]
            text = entry["content"]
            voice = "alloy" if role == "Host" else "nova"

            # Call OpenAI's TTS API
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )

            # Log the response for debugging
            print(f"Response for {role}: {response}")

            # Check if the response is in the expected format
            if hasattr(response, 'content') and isinstance(response.content, bytes):
                audio_file_path = os.path.join(st.runtime.get_instance().temp_dir, f"{role.lower()}_output_{index}.mp3")
                with open(audio_file_path, 'wb') as f:
                    f.write(response.content)

                if os.path.exists(audio_file_path):
                    print(f"Audio file created: {audio_file_path}")
                    audio_file_paths.append(audio_file_path)
                else:
                    print(f"Failed to create audio file: {audio_file_path}")
            else:
                print("Unexpected response format:", response)
                return None

        # Stitch audio files together using pydub
        stitched_audio = AudioSegment.empty()
        for audio_file in audio_file_paths:
            stitched_audio += AudioSegment.from_file(audio_file)

        stitched_audio_path = os.path.join(st.runtime.get_instance().temp_dir, "stitched_output.mp3")
        stitched_audio.export(stitched_audio_path, format="mp3")

        return stitched_audio_path
    except Exception as e:
        print(f"Error generating audio: {e}")
        return {"error": str(e)}  # Return error message as a dictionary
