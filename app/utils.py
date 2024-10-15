import PyPDF2
import os
import requests
from bs4 import BeautifulSoup

def process_pdf(uploaded_file):
    """
    Extracts text from the uploaded PDF file.

    Args:
        uploaded_file: The uploaded PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        # Read the PDF file
        pdf = PyPDF2.PdfReader(uploaded_file)  # Create a PdfReader instance
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Extract text from each page
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return "Error in PDF processing."
    
    return text.strip()  # Return the extracted text, stripped of leading/trailing whitespace

def extract_text_from_url(url):
    """
    Extracts text from the given URL.

    Args:
        url (str): The URL to extract text from.

    Returns:
        str: The extracted text from the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text = "\n".join([para.get_text() for para in paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from URL: {e}")
        return "Error in URL processing."
