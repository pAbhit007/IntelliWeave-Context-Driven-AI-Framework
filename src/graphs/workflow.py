from typing import Dict, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from src.config.settings import GEMINI_MODEL, GOOGLE_API_KEY
from src.agents.router_agent import RouterAgent
from src.tools.weather_api import WeatherAPI
from src.tools.vector_store import VectorStore

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    route: str
    response: str

class WorkflowGraph:
    def __init__(self):
        self.router = RouterAgent()
        self.weather_api = WeatherAPI()
        self.vector_store = VectorStore()
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0
        )

    def process_weather(self, query: str) -> str:
        """Process weather-related queries"""
        # Extract city from query using LLM
        city_prompt = f"Extract just the city name from: {query}"
        city_response = self.llm.invoke([{"role": "user", "content": city_prompt}])
        city = city_response.content.strip()
        
        # Get weather data
        weather_data = self.weather_api.get_weather(city)
        return self.weather_api.format_weather_data(weather_data)

    def process_document(self, query: str) -> str:
        """Process document-related queries"""
        # Search vector store
        results = self.vector_store.search(query)
        
        # Format context
        context = "\n".join([r["text"] for r in results])
        
        # Generate response using LLM
        prompt = f"""
        Based on the following context, answer the question: {query}
        
        Context:
        {context}
        """
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content

    def create_graph(self) -> StateGraph:
        """Create the workflow graph"""
        
        # Define node functions
        def route_node(state: State) -> State:
            query = state["query"]
            route_result = self.router.route_query(query)
            return {"route": route_result[0], "query": route_result[1]}

        def process_node(state: State) -> State:
            if state["route"] == "weather":
                result = self.process_weather(state["query"])
            else:
                result = self.process_document(state["query"])
            return {"response": result}

        # Create workflow
        workflow = StateGraph(State)
        
        # Add nodes
        workflow.add_node("router", route_node)
        workflow.add_node("processor", process_node)
        
        # Add edges
        workflow.add_edge("router", "processor")
        workflow.add_edge("processor", END)
        workflow.set_entry_point("router")
        
        return workflow.compile()

    def run(self, query: str) -> Dict:
        """Run the workflow"""
        graph = self.create_graph()
        result = graph.invoke({"query": query, "messages": []})
        return result
