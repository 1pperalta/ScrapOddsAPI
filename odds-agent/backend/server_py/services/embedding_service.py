"""
Embedding Service

Handles text-to-vector conversion using sentence-transformers.
Converts documents into embeddings for storage in vector database.
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np


class EmbeddingService:
    """Service for generating text embeddings"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to load model only once"""
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the embedding model (loads once)"""
        if self._model is None:
            print("Loading embedding model (this may take a moment on first run)...")
            # Multilingual model that supports Spanish and English
            self._model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
            print("Embedding model loaded successfully")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Convert a single text string to embedding vector
        
        Args:
            text: Text to embed
            
        Returns:
            768-dimensional embedding vector
        """
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple texts to embeddings (batch processing)
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.tolist()
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a query string (semantically same as embed_text, but clearer intent)
        
        Args:
            query: Query text to embed
            
        Returns:
            768-dimensional embedding vector
        """
        return self.embed_text(query)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model"""
        return self._model.get_sentence_embedding_dimension()


# Global instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the global embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def main():
    """Test embedding service"""
    service = get_embedding_service()
    
    # Test single embedding
    test_text = "Arsenal está en gran forma con 4 victorias consecutivas"
    embedding = service.embed_text(test_text)
    
    print(f"Text: {test_text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    
    # Test batch embedding
    test_texts = [
        "Real Madrid ganó 3-1",
        "Barcelona empató 2-2"
    ]
    embeddings = service.embed_texts(test_texts)
    print(f"\nBatch embedded {len(embeddings)} texts")


if __name__ == "__main__":
    main()

