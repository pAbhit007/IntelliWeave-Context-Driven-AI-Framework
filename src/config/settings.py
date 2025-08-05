from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Vector Store Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "knowledge_base"

# LangSmith Configuration
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = "weather_rag_system"

# LLM Configuration
GEMINI_MODEL = "gemini-1.5-flash"  # Updated to current model name
# EMBEDDING_MODEL = "models/embedding-001"


EMBEDDING_MODEL = "text-embedding-ada-002"
