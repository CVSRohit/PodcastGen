import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment  # Import AudioSegment for audio manipulation
import subprocess

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_audio(dialogue):
    """
    Generates audio from the given structured dialogue using OpenAI's TTS model.

    Args:
        dialogue (dict): The structured dialogue containing roles and their respective content.

    Returns:
        str: The path to the stitched audio file.
    """
    audio_file_paths = []  # List to store paths of generated audio files
    try:
        for index, entry in enumerate(dialogue["dialogue"]):  # Use enumerate to get the index
            role = entry["role"]
            text = entry["content"]
            voice = "alloy" if role == "Host" else "nova"  # Specify different voices for roles

            # Call OpenAI's TTS API
            response = client.audio.speech.create(
                model="tts-1",  # Ensure this is the correct model name
                voice=voice,     # Use the specified voice based on the role
                input=text       # The text to convert to audio
            )

            # Check if the response is in the expected format
            if hasattr(response, 'content') and isinstance(response.content, bytes):
                # Save the audio to a file
                audio_file_path = os.path.join(tempfile.gettempdir(), f"{role.lower()}_output_{index}.mp3")  # Include index in filename
                with open(audio_file_path, 'wb') as f:  # Open the file in binary write mode
                    f.write(response.content)  # Write the response content directly to the file
                
                # Check if the file was created successfully
                if os.path.exists(audio_file_path):
                    print(f"Audio file created: {audio_file_path}")
                else:
                    print(f"Failed to create audio file: {audio_file_path}")

                audio_file_paths.append(audio_file_path)  # Add the file path to the list
            else:
                print("Unexpected response format:", response)
                return None  # Return None if the response is not valid

        # Stitch audio files together using pydub
        stitched_audio = AudioSegment.empty()  # Create an empty audio segment
        for audio_file in audio_file_paths:
            stitched_audio += AudioSegment.from_file(audio_file)  # Append each audio file

        # Save the stitched audio to a single file
        stitched_audio_path = os.path.join(tempfile.gettempdir(), "stitched_output.mp3")
        stitched_audio.export(stitched_audio_path, format="mp3")  # Export as MP3

        return stitched_audio_path  # Return the path to the stitched audio file
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
