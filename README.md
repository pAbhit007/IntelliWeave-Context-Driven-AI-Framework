# IntelliWeave-Context-Driven-AI-Framework

This project implements an agentic pipeline using LangGraph with two main functionalities:
1. **Weather API Integration**: Fetches real-time weather data using OpenWeatherMap API
2. **RAG System**: Answers questions from PDF documents using Retrieval-Augmented Generation

## Architecture

The system uses:
- **LangGraph**: For orchestrating the agentic workflow
- **Google Gemini**: As the Large Language Model via LangChain
- **Qdrant**: Vector database for storing document embeddings
- **OpenWeatherMap API**: For real-time weather data
- **Streamlit**: Web UI for chat interface
- **LangSmith**: For LLM response evaluation and tracing

## Project Structure

```
SRC_AYU/
├── src/
│   ├── agents/          # Router agent for decision making
│   ├── config/          # Configuration and settings
│   ├── graphs/          # LangGraph workflow implementation
│   ├── tools/           # Weather API, PDF loader, vector store
│   └── ui/              # Streamlit web interface
├── data/
│   └── documents/       # PDF documents for RAG
├── tests/               # Comprehensive test suite
├── main.py             # CLI application entry point
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root:

```bash
# Google AI API Key (for Gemini LLM and embeddings)
GOOGLE_API_KEY=your_google_api_key_here

# OpenWeatherMap API Key
OPENWEATHER_API_KEY=your_openweather_api_key_here

# LangSmith API Key (for evaluation and tracing)
LANGCHAIN_API_KEY=your_langchain_api_key_here

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333

# LangSmith Project Name
LANGCHAIN_PROJECT=weather_rag_system
```

### 3. Get API Keys

#### Google AI API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

#### OpenWeatherMap API Key:
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to your `.env` file

#### LangSmith API Key (Optional):
1. Sign up at [LangSmith](https://smith.langchain.com/)
2. Create an API key
3. Add it to your `.env` file

### 4. Start Qdrant Vector Database

Using Docker (recommended):
```bash
docker run -d -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

Alternative: Install locally:
```bash
# Follow instructions at https://qdrant.tech/documentation/quick-start/
```

### 5. Initialize Knowledge Base

The system includes a sample PDF in `data/documents/`. To add your own PDFs:

1. Place PDF files in `data/documents/`
2. Run the initialization:

```bash
python main.py
```

## Running the Application

### Option 1: Command Line Interface

```bash
python main.py
```

### Option 2: Streamlit Web Interface

```bash
source venv/bin/activate
streamlit run src/ui/streamlit_app.py
```

The web interface will be available at `http://localhost:8501`

## Testing

Run the comprehensive test suite:

```bash
python run_tests.py
```

Or run specific test modules:

```bash
python -m pytest tests/test_weather_api.py -v
python -m pytest tests/test_router_agent.py -v
python -m pytest tests/test_pdf_loader.py -v
python -m pytest tests/test_vector_store.py -v
python -m pytest tests/test_workflow.py -v
```

## Usage Examples

### Weather Queries:
- "What's the weather like in London?"
- "Give me the current weather in New York"
- "How's the weather in Tokyo today?"

### Document Queries:
- "Tell me about artificial intelligence"
- "What is machine learning?"
- "Explain the technology trends mentioned in the documents"

## Features

### ✅ Implemented Features:

1. **LangGraph Workflow**: Complete agentic pipeline with routing logic
2. **Weather API Integration**: Real-time weather data from OpenWeatherMap
3. **RAG System**: PDF document processing and question answering
4. **Router Agent**: Intelligent decision making between weather and document queries
5. **Vector Database**: Qdrant integration for similarity search
6. **LLM Integration**: Google Gemini for natural language processing
7. **Web Interface**: Clean Streamlit chat interface
8. **Comprehensive Testing**: Unit tests for all components
9. **Modular Architecture**: Clean, maintainable codebase

### 🔄 LangSmith Integration:

The system is configured for LangSmith tracing and evaluation. Set your `LANGCHAIN_API_KEY` to enable:
- Request/response logging
- Performance monitoring
- Chain execution tracing

## Troubleshooting

### Common Issues:

1. **Qdrant Connection Error**:
   - Ensure Qdrant is running: `docker ps`
   - Check port 6333 is available

2. **API Key Errors**:
   - Verify `.env` file exists and has correct keys
   - Check API key permissions and quotas

3. **Import Errors**:
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

4. **PDF Loading Issues**:
   - Check PDF files exist in `data/documents/`
   - Ensure PDFs are readable (not password protected)

### Docker Commands:

```bash
# Check Qdrant status
docker ps

# View Qdrant logs
docker logs [container_id]

# Stop Qdrant
docker stop [container_id]

# Restart Qdrant
docker run -d -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

## Development

To extend the system:

1. **Add new tools**: Create modules in `src/tools/`
2. **Modify routing**: Update `src/agents/router_agent.py`
3. **Extend workflow**: Modify `src/graphs/workflow.py`
4. **Add tests**: Create test files in `tests/`

## Performance Considerations

- **Vector Database**: Qdrant provides fast similarity search
- **Caching**: LangChain provides built-in caching for LLM calls
- **Chunking**: Documents are split into optimal chunks for retrieval
- **Async Support**: Framework supports async operations for scalability

## License

This project is part of an AI Engineer assignment and is for educational purposes.
