from typing import List, Dict
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.config.settings import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, GOOGLE_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=GOOGLE_API_KEY,
            model="models/embedding-001"
        )
        self._create_collection()

    def _create_collection(self):
        """
        Create or validate collection existence
        """
        try:
            self.client.get_collection(COLLECTION_NAME)
        except:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=768,  # Google embedding-001 dimension
                    distance=models.Distance.COSINE
                )
            )

    def store_documents(self, documents: List):
        """
        Store documents in vector store
        """
        for doc in documents:
            vector = self.embeddings.embed_query(doc.page_content)
            # Generate a UUID for the point ID to ensure it's valid
            point_id = str(uuid.uuid4())
            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={"text": doc.page_content, "metadata": doc.metadata}
                    )
                ]
            )

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for similar documents
        """
        query_vector = self.embeddings.embed_query(query)
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit
        )
        return [{"text": hit.payload["text"], "score": hit.score} for hit in results]
