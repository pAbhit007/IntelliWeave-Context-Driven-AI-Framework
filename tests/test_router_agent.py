import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.router_agent import RouterAgent

class TestRouterAgent(unittest.TestCase):
    def setUp(self):
        self.router = RouterAgent()

    @patch('src.agents.router_agent.ChatGoogleGenerativeAI')
    def test_route_weather_query(self, mock_llm_class):
        # Mock LLM response
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "weather"
        mock_llm.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm
        
        router = RouterAgent()
        router.llm = mock_llm
        
        result = router.route_query("What's the weather in London?")
        
        self.assertEqual(result[0], "weather")
        self.assertEqual(result[1], "What's the weather in London?")

    @patch('src.agents.router_agent.ChatGoogleGenerativeAI')
    def test_route_document_query(self, mock_llm_class):
        # Mock LLM response
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "document"
        mock_llm.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm
        
        router = RouterAgent()
        router.llm = mock_llm
        
        result = router.route_query("Tell me about AI from the documents")
        
        self.assertEqual(result[0], "document")
        self.assertEqual(result[1], "Tell me about AI from the documents")

    @patch('src.agents.router_agent.ChatGoogleGenerativeAI')
    def test_route_invalid_response_defaults_to_document(self, mock_llm_class):
        # Mock LLM response
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "invalid_response"
        mock_llm.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm
        
        router = RouterAgent()
        router.llm = mock_llm
        
        result = router.route_query("Some ambiguous query")
        
        self.assertEqual(result[0], "document")
        self.assertEqual(result[1], "Some ambiguous query")

if __name__ == '__main__':
    unittest.main()