import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st  # Add this import to use Streamlit for input
from pydantic import BaseModel  # Add this import for Pydantic models

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the structured output classes
class Step(BaseModel):
    explanation: str
    output: str

class PodcastDialogue(BaseModel):
    steps: list[Step]
    final_dialogue: dict

def summarize_text(text, audience, host_name, guest_name):
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

    try:
        messages = [
            {"role": "user", "content": f"Please summarize in maximum 750 words the following text into a structured podcast dialogue between host {host_name} and guest {guest_name}. Example, 'Host: Hello and welcome to SummarizeToday' and ''. One dialogue per line. No formatting like bold, italic, or bullet points. The audience for this podcast is {audience}. Name of the podcast is SummarizeToday. Here are some grounding examples:\n\n"
             "1. Host: Welcome to SummarizeToday! I'm your host, John, and today we have a special guest, Ash.\n"
             "   Guest: Thanks for having me, John! I'm excited to be here.\n"
             "2. Host: Hello everyone, this is John, and you're listening to SummarizeToday. Today, we have Ash with us.\n"
             "   Guest: Hi John! It's great to be on the show.\n"
             "3. Host: Welcome back to SummarizeToday! I'm John, your host, and today we have Ash joining us.\n"
             "   Guest: Thanks, John! I'm thrilled to discuss this topic.\n"
             "4. Host: Hi everyone, this is John from SummarizeToday. Today, we have Ash here to discuss an exciting topic.\n"
             "   Guest: Thanks for having me, John! I'm looking forward to our conversation.\n\n"
             f"Now, please summarize the following text:\n\n{text}"}
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
        structured_dialogue = PodcastDialogue(steps=[], final_dialogue={"dialogue": []})
        
        # Assuming the response is formatted as "Host: [text] Guest: [text]"
        for line in podcast_dialogue.splitlines():
            if line.startswith("**Host:**") or line.startswith("Host:") or line.startswith("**Host: ${host_name}**"):
                structured_dialogue.final_dialogue["dialogue"].append({"role": "Host", "content": line[10:].strip()})
                structured_dialogue.steps.append(Step(explanation=f"Host speaks: {line[10:].strip()}", output=line[10:].strip()))
            elif line.startswith("**Guest:**") or line.startswith("Guest:") or line.startswith("**Guest: ${guest_name}**"):
                structured_dialogue.final_dialogue["dialogue"].append({"role": "Guest", "content": line[11:].strip()})
                structured_dialogue.steps.append(Step(explanation=f"Guest speaks: {line[11:].strip()}", output=line[11:].strip()))

        print("API Response:", podcast_dialogue)  # Log the API response

        return structured_dialogue  # Return structured dialogue as a dictionary
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return {"error": "Error in summarization."}
