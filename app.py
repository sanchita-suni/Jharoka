import streamlit as st
import os
import subprocess
import sys

# Function to ensure a package is installed
def ensure_package_installed(package_name):
    """Checks if a package is installed and installs it if not."""
    try:
        __import__(package_name)
    except ImportError:
        st.error(f"The required '{package_name}' library is not installed. Attempting to install...")
        # Use subprocess to run pip installation
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        st.success(f"Successfully installed '{package_name}'. Please relaunch the application.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while checking for '{package_name}': {e}")
        st.stop()

# Ensure all necessary packages are installed
try:
    ensure_package_installed("streamlit")
    ensure_package_installed("chromadb")
    ensure_package_installed("sentence-transformers")
    ensure_package_installed("replicate")
    ensure_package_installed("requests")
    ensure_package_installed("beautifulsoup4")
except Exception as e:
    st.error(f"Failed to install a required package. Please check your internet connection or terminal permissions. Error: {e}")
    st.stop()

# Import your custom modules after ensuring they are available
from modules.database import add_artisan, search_artisans
from modules.ai_chain import transcribe_audio, generate_mockup_images
from modules.price_data import get_price_data

# Set up the page configuration
st.set_page_config(
    page_title="Artisan Portal",
    page_icon=":art:",
    layout="centered"
)

def display_search_results(results):
    """
    Displays the search results in the UI.
    """
    if not results or not results.get('ids'):
        st.info("No artisans found matching your search query.")
        return

    st.subheader("Search Results")
    for i in range(len(results['ids'])):
        artisan_id = results['ids'][i][0] # Access the ID from the nested list
        metadata = results['metadatas'][i][0] # Access the metadata
        profile = metadata.get('profile', {})
        images = metadata.get('images', [])
        document_text = results['documents'][i][0]
        
        with st.expander(f"Artisan: {profile.get('essence', 'Unknown Artisan')}"):
            st.markdown(f"**English Profile:** {profile.get('profile_en')}")
            st.markdown(f"**Hindi Profile:** {profile.get('profile_hi')}")
            st.markdown(f"**Kannada Profile:** {profile.get('profile_kn')}")
            
            st.markdown("**Image Mockups:**")
            if images:
                cols = st.columns(len(images))
                for idx, img_url in enumerate(images):
                    with cols[idx]:
                        st.image(img_url, caption=f"Mockup {idx+1}", use_column_width=True)
            else:
                st.info("No images available for this artisan.")

def artisan_portal_ui():
    """
    Builds the UI for Samika's Artisan Portal task.
    """
    st.header("Artisan Portal")
    st.markdown("Upload a profile image and an audio file to create a new artisan profile.")

    # File uploaders for the image and audio file
    image_file = st.file_uploader("Upload Profile Image", type=["jpg", "png"], key="image_uploader")
    audio_file = st.file_uploader("Upload Audio Profile", type=["mp3", "wav"], key="audio_uploader")

    # The button that triggers the pipeline
    if st.button("Submit Artisan Profile", key="submit_button"):
        if image_file and audio_file:
            # Display a spinner to show that the process is running
            with st.spinner("Processing your profile..."):
                try:
                    # Step 1: Transcribe the audio file
                    st.info("Transcribing audio...")
                    audio_bytes = audio_file.read()
                    transcribed_text = transcribe_audio(audio_bytes)
                    st.success("Audio transcribed successfully!")

                    # Placeholder for getting content from Gemini.
                    st.info("Generating content with Gemini (Mock)...")
                    profile_data = {
                        "essence": "Master Artisan",
                        "profile_en": transcribed_text,
                        "profile_hi": "नमस्ते, मैं एक कुशल कारीगर हूँ।",
                        "profile_kn": "ನಮಸ್ತೆ, ನಾನು ಒಬ್ಬ ನುರಿತ ಕುಶಲಕರ್ಮಿ."
                    }
                    image_urls = ["https://placehold.co/400x400/007bff/ffffff?text=Mockup+1", "https://placehold.co/400x400/ff6347/ffffff?text=Mockup+2"]

                    # Step 2: Add the artisan data to the database
                    st.info("Adding profile to the database...")
                    add_artisan(profile_data, image_urls)
                    st.success("Profile added to database!")

                    st.balloons()
                    st.success("Artisan profile created and stored successfully!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload both an image and an audio file to proceed.")

def main_app():
    """
    This function sets up the overall Streamlit app structure.
    """
    st.title("Artisan Connect")
    st.sidebar.title("Navigation")
    
    # Placeholder for the language selector, to be implemented by San
    selected_language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Kannada"])
    st.sidebar.info(f"Language selected: {selected_language}")
    
    # Placeholder for different sections in the app
    # Samika's section
    artisan_portal_ui()
    
    # Placeholder for Riddhi's "Designer Studio"
    st.header("Designer Studio")
    search_query = st.text_input("Search for artisans...")
    if st.button("Search"):
        if search_query:
            results = search_artisans(search_query)
            display_search_results(results)
        else:
            st.warning("Please enter a search query.")
            
    # New section for the Market Price Tool
    st.sidebar.markdown("---")
    st.sidebar.header("Market Price Tool")
    price_query = st.sidebar.text_input("Enter product name:")
    if st.sidebar.button("Get Price Data"):
        if price_query:
            with st.spinner("Fetching market data..."):
                try:
                    price_data = get_price_data(price_query)
                    st.sidebar.subheader("Results:")
                    st.sidebar.json(price_data)
                except Exception as e:
                    st.sidebar.error(f"An error occurred: {e}")
        else:
            st.sidebar.warning("Please enter a product name.")

if __name__ == "__main__":
    main_app()

