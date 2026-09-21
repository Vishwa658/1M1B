import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# Groq AI Configuration
# ==============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


# ==============================
# Groundwater / RAG Configuration
# ==============================

GROUNDWATER_DATA_DIR = "data"

RAG_INDEX_PATH = "rag/faiss.index"

RAG_METADATA_PATH = "rag/metadata.pkl"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

TOP_K_DOCUMENTS = 4