from typing import Dict, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.config.settings import GEMINI_MODEL, GOOGLE_API_KEY

class RouterAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0
        )

    def route_query(self, query: str) -> Tuple[str, str]:
        """
        Determine whether to route to weather or RAG pipeline
        """
        prompt = f"""
        Determine if the following query is asking about weather or requesting information from documents.
        Query: {query}
        
        Return exactly one word: either 'weather' or 'document'
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        route = response.content.strip().lower()
        
        return (route, query) if route in ['weather', 'document'] else ('document', query)
