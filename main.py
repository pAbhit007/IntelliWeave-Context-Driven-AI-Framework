from src.graphs.workflow import WorkflowGraph
from src.tools.pdf_loader import PDFLoader
from src.tools.vector_store import VectorStore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_knowledge_base():
    """Initialize the knowledge base with PDF documents"""
    pdf_loader = PDFLoader()
    vector_store = VectorStore()
    
    # Load PDFs from the documents directory
    docs_dir = os.path.join(os.path.dirname(__file__), "data", "documents")
    for filename in os.listdir(docs_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(docs_dir, filename)
            chunks = pdf_loader.load_and_split(pdf_path)
            vector_store.store_documents(chunks)

def check_api_keys():
    """Check if required API keys are set"""
    required_keys = {
        'GOOGLE_API_KEY': 'Google AI API key for LLM and embeddings',
        'OPENWEATHER_API_KEY': 'OpenWeatherMap API key for weather data'
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(f"  - {key}: {description}")
    
    if missing_keys:
        print("❌ Missing required API keys in .env file:")
        for key in missing_keys:
            print(key)
        print("\nPlease add these to your .env file and try again.")
        print("Get API keys from:")
        print("  - Google AI: https://makersuite.google.com/app/apikey")
        print("  - OpenWeather: https://openweathermap.org/api")
        return False
    
    print("✅ All required API keys found")
    return True

def main():
    print("🚀 Starting AI Engineer Assignment - LangGraph Agentic Pipeline")
    print("=" * 60)
    
    # Check API keys first
    if not check_api_keys():
        return
    
    try:
        # Initialize the knowledge base
        print("\n📚 Initializing knowledge base...")
        initialize_knowledge_base()
        print("✅ Knowledge base initialized successfully")
        
        # Create workflow instance
        print("\n🔗 Creating workflow...")
        workflow = WorkflowGraph()
        print("✅ Workflow created successfully")
        
        # Example usage
        print("\n💬 Testing queries...")
        
        query = "What's the weather like in London?"
        print(f"\nQuery: {query}")
        result = workflow.run(query)
        print(f"Response: {result['response']}")
        
        query = "Tell me about artificial intelligence"
        print(f"\nQuery: {query}")
        result = workflow.run(query)
        print(f"Response: {result['response']}")
        
        print(f"\n🎉 Success! The application is working correctly.")
        print("💡 Try running the Streamlit UI: streamlit run src/ui/streamlit_app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("  1. Make sure Qdrant is running: docker run -d -p 6333:6333 qdrant/qdrant")
        print("  2. Check your API keys in .env file")
        print("  3. Ensure you're in the virtual environment: source venv/bin/activate")

if __name__ == "__main__":
    main()
