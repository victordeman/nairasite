import logging
import anyio
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    async def build_index(self, data: list[str]):
        """
        Builds a FAISS index from a list of strings.
        """
        if not data:
            logger.warning("No data provided to build RAG index.")
            return

        self.documents = data
        # Run synchronous embedding in a separate thread to avoid blocking the event loop
        embeddings = await anyio.to_thread.run_sync(self.model.encode, data)

        # Convert to float32 for FAISS
        embeddings = np.array(embeddings).astype('float32')

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        logger.info(f"RAG index built with {len(data)} documents.")

    async def query(self, query_text: str, top_k: int = 3) -> list[str]:
        """
        Queries the FAISS index and returns the top_k relevant documents.
        """
        if self.index is None or not self.documents:
            logger.warning("RAG index not initialized.")
            return []

        # Run synchronous embedding in a separate thread to avoid blocking the event loop
        query_embedding_list = await anyio.to_thread.run_sync(self.model.encode, [query_text])
        query_embedding = np.array(query_embedding_list).astype('float32')

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx])

        return results

# Singleton instance
rag_manager = RAGManager()
