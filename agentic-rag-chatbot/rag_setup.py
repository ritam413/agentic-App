# rag_setup.py

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_faiss_index(file_path, index_path="faiss_index"):
    """
    Loads a document, splits it into chunks, and creates a local FAISS vector store.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    # Load the document
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Initialize the embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create the FAISS vector store and save it
    vector_store = FAISS.from_documents(docs, embedding_model)
    vector_store.save_local(index_path)

    print(f"✅ FAISS index created and saved at: {index_path}")

if __name__ == "__main__":
    # Make sure the file name matches exactly (knowledge.txt, not knolege.txt)
    create_faiss_index("data/knowledge.txt")
