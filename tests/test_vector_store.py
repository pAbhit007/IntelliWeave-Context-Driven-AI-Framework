import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.vector_store import VectorStore

class TestVectorStore(unittest.TestCase):
    
    @patch('src.tools.vector_store.QdrantClient')
    @patch('src.tools.vector_store.GoogleGenerativeAIEmbeddings')
    def test_vector_store_initialization(self, mock_embeddings, mock_client):
        """Test VectorStore initialization"""
        # Mock the client and embeddings
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        # Mock collection existence check
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        
        vector_store = VectorStore()
        
        # Verify initialization
        self.assertIsNotNone(vector_store.client)
        self.assertIsNotNone(vector_store.embeddings)
        mock_client_instance.create_collection.assert_called_once()

    @patch('src.tools.vector_store.QdrantClient')
    @patch('src.tools.vector_store.GoogleGenerativeAIEmbeddings')
    def test_store_documents(self, mock_embeddings, mock_client):
        """Test storing documents in vector store"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        
        # Mock embedding response
        mock_embeddings_instance.embed_query.return_value = [0.1] * 768
        
        vector_store = VectorStore()
        
        # Mock document
        mock_doc = Mock()
        mock_doc.page_content = "Test content"
        mock_doc.metadata = {"source": "test.pdf"}
        
        vector_store.store_documents([mock_doc])
        
        # Verify embedding was called
        mock_embeddings_instance.embed_query.assert_called_with("Test content")
        # Verify upsert was called
        mock_client_instance.upsert.assert_called_once()

    @patch('src.tools.vector_store.QdrantClient')
    @patch('src.tools.vector_store.GoogleGenerativeAIEmbeddings')
    def test_search_documents(self, mock_embeddings, mock_client):
        """Test searching documents in vector store"""
        # Setup mocks
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        
        # Mock embedding response
        mock_embeddings_instance.embed_query.return_value = [0.1] * 768
        
        # Mock search results
        mock_hit = Mock()
        mock_hit.payload = {"text": "AI is important", "metadata": {}}
        mock_hit.score = 0.95
        mock_client_instance.search.return_value = [mock_hit]
        
        vector_store = VectorStore()
        
        results = vector_store.search("artificial intelligence")
        
        # Verify search was performed
        mock_embeddings_instance.embed_query.assert_called_with("artificial intelligence")
        mock_client_instance.search.assert_called_once()
        
        # Verify results format
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "AI is important")
        self.assertEqual(results[0]["score"], 0.95)

if __name__ == '__main__':
    unittest.main()