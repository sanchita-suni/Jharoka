import chromadb
from chromadb.utils import embedding_functions

# Initialize the ChromaDB client. We use PersistentClient to save data
# to a local directory so it doesn't get lost when you close the app.
# The `path` parameter specifies where the database files will be stored.
client = chromadb.PersistentClient(path="./chroma_db")

# ChromaDB needs an embedding function to turn text into vectors.
# We will use the default SentenceTransformer model provided by ChromaDB.
# This is a pre-trained model that works well for many tasks.
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# A 'collection' in ChromaDB is similar to a table in a traditional database.
# This line creates the collection if it doesn't already exist.
# The embedding_function tells the collection how to convert text into embeddings.
collection = client.get_or_create_collection(
    "artisans", embedding_function=sentence_transformer_ef
)

def add_artisan(profile_data: dict, image_urls: list):
    """
    Creates a text embedding from the profile data and stores all the
    metadata in the ChromaDB collection.

    Args:
        profile_data (dict): A dictionary containing the artisan's profile information.
        image_urls (list): A list of image URLs related to the artisan.
    """
    # We will use the English profile text as the document to embed.
    # The 'document' is the text that ChromaDB will turn into a vector.
    document = profile_data.get("profile_en", "")

    # We need a unique ID for each document. The 'essence' field is a good choice.
    artisan_id = profile_data.get("essence", "unknown_artisan")

    # The 'metadatas' field can store any additional information you need.
    # We'll store the full profile data and image URLs here.
    metadata = {
        "profile": profile_data,
        "images": image_urls
    }

    try:
        # The add() method adds the document, metadata, and ID to the collection.
        # ChromaDB automatically creates the embedding for the document.
        collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[artisan_id]
        )
        print(f"Successfully added artisan: {artisan_id}")
    except Exception as e:
        print(f"Error adding artisan {artisan_id}: {e}")

def search_artisans(query_text: str) -> list:
    """
    Handles embedding the query and searching the ChromaDB for similar artisans.

    Args:
        query_text (str): The search query text.

    Returns:
        list: A list of search results.
    """
    try:
        # The query() method searches for documents that are semantically
        # similar to the query_text.
        # n_results=5 means we want the top 5 most similar results.
        results = collection.query(
            query_texts=[query_text],
            n_results=5
        )
        print(f"Search results for '{query_text}': {results}")
        return results
    except Exception as e:
        print(f"Error searching for '{query_text}': {e}")
        return []

if __name__ == "__main__":
    # This block is for testing the functions independently.
    # It won't run when you import this file into app.py.

    # Example profile data
    sample_profile = {
        "essence": "Master Weaver",
        "profile_en": "An artisan specializing in traditional hand-woven textiles using natural dyes.",
        "profile_hi": "एक कारीगर जो प्राकृतिक रंगों का उपयोग करके पारंपरिक हाथ से बुने हुए वस्त्रों में विशेषज्ञता रखता है।",
        "profile_kn": "ಒಬ್ಬ ಕುಶಲಕರ್ಮಿ, ಅವರು ನೈಸರ್ಗಿಕ ಬಣ್ಣಗಳನ್ನು ಬಳಸಿಕೊಂಡು ಸಾಂಪ್ರದಾಯಿಕ ಕೈಮಗ್ಗದ ಜವಳಿಗಳಲ್ಲಿ ಪರಿಣತಿ ಹೊಂದಿದ್ದಾರೆ."
    }
    sample_images = ["url1.jpg", "url2.jpg"]

    # Add the sample artisan to the database
    add_artisan(sample_profile, sample_images)

    # Search for a similar artisan
    search_artisans("A person who creates textiles by hand with organic colors.")
