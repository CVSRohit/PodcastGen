import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st  # Add this import to use Streamlit for input

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, audience, host_name=None, guest_name=None):
    """
    Summarizes the given text using OpenAI's GPT model and formats it as a structured podcast dialogue.

    Args:
        text (str): The text to summarize.
        audience (str): The audience definition for the podcast.
        host_name (str): The name of the host.
        guest_name (str): The name of the guest.

    Returns:
        dict: A structured representation of the podcast dialogue.
    """
    # Set default values if host_name or guest_name are not provided
    host_name = host_name or "John"
    guest_name = guest_name or "Ash"

    try:
        messages = [
            {"role": "user", "content": f"Please summarize in maximum 750 words the following text into a structured podcast dialogue between {host_name} and {guest_name}. The audience for this podcast is {audience}. Name of the podcast is SummarizeToday:\n\n{text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )

        # Check if response has choices and content
        if response.choices and hasattr(response.choices[0], 'message'):
            podcast_dialogue = response.choices[0].message.content
        else:
            print("Unexpected response format:", response)
            return {"error": "Unexpected response format."}
        
        # New structured output
        structured_dialogue = {
            "dialogue": []
        }
        
        # Assuming the response is formatted as "Host: [text] Guest: [text]"
        for line in podcast_dialogue.splitlines():
            if line.startswith("**Host:") or line.startswith("Host:"):
                structured_dialogue["dialogue"].append({"role": "Host", "content": line[10:].strip()})
            elif line.startswith("**Guest:") or line.startswith("Guest:"):
                structured_dialogue["dialogue"].append({"role": "Guest", "content": line[11:].strip()})

        print("API Response:", podcast_dialogue)  # Log the API response

        return structured_dialogue  # Return structured dialogue without Streamlit code
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return {"error": "Error in summarization."}
