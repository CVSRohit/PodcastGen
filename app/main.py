import streamlit as st
from utils import process_pdf, extract_text_from_url
from summarizer import summarize_text, PodcastDialogue
from tts import generate_audio

st.set_page_config(page_title="SummarizeToday", page_icon="app/podcast.png")  # Changed to use podcast image

def main():
    # Initialize session state variables if they don't exist
    if 'show_edit' not in st.session_state:
        st.session_state.show_edit = False  # Initialize show_edit to False

    # Display the title with the image next to it
    st.image("app/podcast.png", width=50)  # Adjust width as needed
    st.title("SummarizeToday: PDF/Link to Podcast")  # Replace with your actual title
    
    # Create two columns for file upload and URL input
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        # File upload
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    with col2:
        # URL input
        url = st.text_input("Or enter a URL to summarize:")
    
    text = None  # Initialize text variable

    # Add input for audience definition
    audience = st.text_input("Define the audience for the podcast (e.g, CEO of an AI company):")

    # Create a new row for host and guest names
    col3, col4 = st.columns(2)  # Create two new columns for host and guest names

    with col3:
        # Add input for host name
        host_name = st.text_input("Enter the host's name:", value="John")

    with col4:
        # Add input for guest name
        guest_name = st.text_input("Enter the guest's name:", value="Ash")

    # Define host and guest names
    # host_name = "John"  # Set host name
    # guest_name = "Ash"  # Set guest name

    if uploaded_file is not None:
        # Process the PDF
        text = process_pdf(uploaded_file)
    elif url:
        # Extract text from the URL
        text = extract_text_from_url(url)

    if text:
        st.markdown("<span style='color: green;'>Text Extraction status: Success</span>", unsafe_allow_html=True)

        # Generate the "Generate Dialogues" button only if text is available
        if st.button("Generate Dialogues"):
            # Summarize the text into podcast dialogue, passing the audience, host, and guest names
            podcast_dialogue = summarize_text(text, audience, host_name, guest_name)
            if isinstance(podcast_dialogue, PodcastDialogue):  # Check if it's already a PodcastDialogue object
                st.session_state.podcast_dialogue = podcast_dialogue
                st.success("Dialogues generated successfully!")
            elif isinstance(podcast_dialogue, dict) and "error" not in podcast_dialogue:
                st.session_state.podcast_dialogue = PodcastDialogue(**podcast_dialogue)
                st.success("Dialogues generated successfully!")
            else:
                st.error(podcast_dialogue.get("error", "An unknown error occurred"))

        # Display the dialogue in a text format
        if 'podcast_dialogue' in st.session_state:
            if not st.session_state.show_edit:
                st.write("### Generated Dialogue:")
                # Use updated dialogue if available
                dialogue_to_display = st.session_state.get('updated_dialogue', st.session_state.podcast_dialogue.final_dialogue["dialogue"])
                for entry in dialogue_to_display:
                    st.write(f"**{entry['role']}:** {entry['content']}")

            # Add an Edit button
            if st.button("Edit Dialogue"):
                st.session_state.show_edit = True

            # Show edit box and Save Changes button when Edit is clicked
            if st.session_state.get('show_edit', False):
                # Combine all dialogues into one string
                combined_dialogue = "\n".join([f"{entry['role']}: {entry['content']}" for entry in st.session_state.podcast_dialogue.final_dialogue["dialogue"]])
                
                # Allow user to edit all dialogues in one text area
                edited_text = st.text_area("Edit the entire dialogue:", value=combined_dialogue, height=300)
                
                # Add a button to save changes
                if st.button("Save Changes"):
                    # Parse the edited text back into structured format
                    new_dialogue = []
                    for line in edited_text.split('\n'):
                        if ':' in line:
                            role, content = line.split(':', 1)
                            new_dialogue.append({"role": role.strip(), "content": content.strip()})
                    
                    st.session_state.podcast_dialogue.final_dialogue["dialogue"] = new_dialogue
                    st.session_state.show_edit = False
                    st.success("Changes saved!")
                    st.session_state.updated_dialogue = new_dialogue  

        # Generate audio from podcast dialogue only if it exists
        if 'podcast_dialogue' in st.session_state and st.button("Generate Podcast"):
            audio_file = generate_audio(st.session_state.podcast_dialogue.final_dialogue)
            if audio_file and isinstance(audio_file, str):  # Check if audio_file is a valid string
                # Use st.audio to play the audio bytes directly
                st.audio(audio_file, format='audio/mp3')
                st.success("Audio generated successfully!")  # Notify user of success
                st.write("Please note that this audio is AI-generated.")
            elif isinstance(audio_file, dict) and "error" in audio_file:  # Check for error in audio generation
                st.error(audio_file["error"])  # Display error message
            else:
                st.error("No audio generated or invalid audio data. Please check the logs for more details.")
    else:
        st.write("No text available for summarization.")

    # Add the Publish to Apple Podcast link at the bottom with limited logo size
    st.markdown(
        "<a href='https://podcasters.apple.com/' target='_blank'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Podcasts_%28iOS%29.svg/50px-Podcasts_%28iOS%29.svg.png' style='width: 40px;'/>Publish to Apple Podcast</a>",
        unsafe_allow_html=True
    )
    
    st.write("Created by [Rohit Challa](https://www.linkedin.com/in/rohitchalla/). Open source on [GitHub](https://github.com/CVSRohit/PodcastGen)")

if __name__ == "__main__":
    main()
