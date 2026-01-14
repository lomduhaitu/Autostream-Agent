import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings # CHANGED
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

def build_retriever():
    print("Loading Knowledge Base...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "knowledge_base.md")
    
    loader = TextLoader(data_path)
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # --- CHANGED: Using Google Embeddings ---
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    db = FAISS.from_documents(docs, embeddings)
    
    print("Knowledge Base Loaded Successfully.")
    return db.as_retriever()

retriever = build_retriever()

@tool
def lookup_policy(query: str):
    """
    Useful for answering questions about AutoStream pricing, plans, features, 
    video limits, resolutions, and refund policies.
    """
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

@tool
def mock_lead_capture(name: str, email: str, platform: str):
    """
    Call this tool ONLY when you have collected the user's Name, Email, and Creator Platform.
    Used to submit a high-intent lead to the backend.
    """
    print(f"\n[SYSTEM ACTION] Lead captured successfully: Name={name}, Email={email}, Platform={platform}\n")
    return "Lead successfully recorded in the system."