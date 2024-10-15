# SummarizeToday: PDF/Link to Podcast

SummarizeToday is a web application that allows users to upload PDF files or enter URLs to summarize content into structured podcast dialogues. The application utilizes OpenAI's GPT model for summarization and TTS (Text-to-Speech) for generating audio from the dialogues.

## Features

- Upload PDF files or enter URLs to extract text.
- Define the audience for the podcast.
- Input host and guest names for personalized dialogues.
- Generate structured podcast dialogues based on the extracted text.
- Edit generated dialogues before finalizing.
- Generate audio from the dialogues using TTS.

## Requirements

- Python 3.7 or higher
- Streamlit
- OpenAI API client
- PyPDF2
- pydub
- requests
- beautifulsoup4
- python-dotenv
- ffmpeg-python

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CVSRohit/PodcastGen.git
   cd PodcastGen
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:

   - Create a `.env` file in the root directory of the project and add your OpenAI API key:

     ```plaintext
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. Run the application:

   ```bash
   streamlit run app/main.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Upload a PDF file or enter a URL to summarize the content.

4. Define the audience, host, and guest names.

5. Click on "Generate Dialogues" to create the podcast dialogue.

6. Edit the dialogue if necessary and click "Save Changes."

7. Generate audio from the dialogues by clicking "Generate Podcast."

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT model and TTS capabilities.
- [Streamlit](https://streamlit.io/) for building the web application interface.
- [PyPDF2](https://github.com/py-pdf/PyPDF2) for PDF text extraction.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.

## Contact

Created by Rohit Challa. For any inquiries, please reach out via [GitHub](https://github.com/CVSRohit).

