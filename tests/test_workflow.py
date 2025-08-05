import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graphs.workflow import WorkflowGraph

class TestWorkflowGraph(unittest.TestCase):
    
    @patch('src.graphs.workflow.RouterAgent')
    @patch('src.graphs.workflow.WeatherAPI')
    @patch('src.graphs.workflow.VectorStore')
    @patch('src.graphs.workflow.ChatGoogleGenerativeAI')
    def test_workflow_initialization(self, mock_llm, mock_vector, mock_weather, mock_router):
        """Test WorkflowGraph initialization"""
        workflow = WorkflowGraph()
        
        self.assertIsNotNone(workflow.router)
        self.assertIsNotNone(workflow.weather_api)
        self.assertIsNotNone(workflow.vector_store)
        self.assertIsNotNone(workflow.llm)

    @patch('src.graphs.workflow.RouterAgent')
    @patch('src.graphs.workflow.WeatherAPI')
    @patch('src.graphs.workflow.VectorStore')
    @patch('src.graphs.workflow.ChatGoogleGenerativeAI')
    def test_process_weather_query(self, mock_llm, mock_vector, mock_weather, mock_router):
        """Test weather query processing"""
        # Setup mocks
        mock_llm_instance = Mock()
        mock_weather_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        mock_weather.return_value = mock_weather_instance
        
        # Mock LLM response for city extraction
        mock_city_response = Mock()
        mock_city_response.content = "London"
        mock_llm_instance.invoke.return_value = mock_city_response
        
        # Mock weather API response
        mock_weather_data = {
            'name': 'London',
            'main': {'temp': 20.5, 'feels_like': 18.2, 'humidity': 65},
            'weather': [{'description': 'clear sky'}]
        }
        mock_weather_instance.get_weather.return_value = mock_weather_data
        mock_weather_instance.format_weather_data.return_value = "Weather in London: 20.5°C, clear sky"
        
        workflow = WorkflowGraph()
        workflow.llm = mock_llm_instance
        workflow.weather_api = mock_weather_instance
        
        result = workflow.process_weather("What's the weather in London?")
        
        # Verify calls
        mock_weather_instance.get_weather.assert_called_with("London")
        mock_weather_instance.format_weather_data.assert_called_with(mock_weather_data)
        self.assertEqual(result, "Weather in London: 20.5°C, clear sky")

    @patch('src.graphs.workflow.RouterAgent')
    @patch('src.graphs.workflow.WeatherAPI')
    @patch('src.graphs.workflow.VectorStore')
    @patch('src.graphs.workflow.ChatGoogleGenerativeAI')
    def test_process_document_query(self, mock_llm, mock_vector, mock_weather, mock_router):
        """Test document query processing"""
        # Setup mocks
        mock_llm_instance = Mock()
        mock_vector_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        mock_vector.return_value = mock_vector_instance
        
        # Mock vector search results
        mock_search_results = [
            {"text": "AI is artificial intelligence", "score": 0.9},
            {"text": "Machine learning is a subset of AI", "score": 0.85}
        ]
        mock_vector_instance.search.return_value = mock_search_results
        
        # Mock LLM response
        mock_llm_response = Mock()
        mock_llm_response.content = "AI refers to artificial intelligence and includes machine learning."
        mock_llm_instance.invoke.return_value = mock_llm_response
        
        workflow = WorkflowGraph()
        workflow.llm = mock_llm_instance
        workflow.vector_store = mock_vector_instance
        
        result = workflow.process_document("What is AI?")
        
        # Verify calls
        mock_vector_instance.search.assert_called_with("What is AI?")
        mock_llm_instance.invoke.assert_called_once()
        self.assertEqual(result, "AI refers to artificial intelligence and includes machine learning.")

    @patch('src.graphs.workflow.RouterAgent')
    @patch('src.graphs.workflow.WeatherAPI')
    @patch('src.graphs.workflow.VectorStore')
    @patch('src.graphs.workflow.ChatGoogleGenerativeAI')
    def test_complete_workflow_weather(self, mock_llm, mock_vector, mock_weather, mock_router):
        """Test complete workflow for weather query"""
        # Setup mocks
        mock_router_instance = Mock()
        mock_weather_instance = Mock()
        mock_llm_instance = Mock()
        
        mock_router.return_value = mock_router_instance
        mock_weather.return_value = mock_weather_instance
        mock_llm.return_value = mock_llm_instance
        
        # Mock router decision
        mock_router_instance.route_query.return_value = ("weather", "What's the weather in London?")
        
        # Mock weather processing
        mock_city_response = Mock()
        mock_city_response.content = "London"
        mock_llm_instance.invoke.return_value = mock_city_response
        
        mock_weather_data = {'name': 'London', 'main': {'temp': 20.5}}
        mock_weather_instance.get_weather.return_value = mock_weather_data
        mock_weather_instance.format_weather_data.return_value = "Weather in London: 20.5°C"
        
        workflow = WorkflowGraph()
        workflow.router = mock_router_instance
        workflow.weather_api = mock_weather_instance
        workflow.llm = mock_llm_instance
        
        result = workflow.run("What's the weather in London?")
        
        # Verify the workflow executed correctly
        self.assertIn("response", result)
        mock_router_instance.route_query.assert_called_with("What's the weather in London?")

if __name__ == '__main__':
    unittest.main()