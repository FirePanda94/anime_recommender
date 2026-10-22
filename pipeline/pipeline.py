from src.vector_store import VectorStoreBuilder
from src.recommender import (
    AnimeRecommender,
)  # Updated to match our direct implementation name
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    def __init__(self, persist_dir="chroma_db"):
        try:
            logger.info("Initializing Recommendation Pipeline...")

            # 1. FIXED: Initialize the builder without a source CSV path (since we are only loading)
            vector_builder = VectorStoreBuilder(csv_path="", persist_dir=persist_dir)
            vector_store = vector_builder.load_vector_store()

            # 2. FIXED: Pass the vector store directly to our modern recommender engine
            # instead of using the legacy retriever-only chain pattern.
            self.recommender = AnimeRecommender(vector_store=vector_store)

            logger.info("Pipeline initialized successfully...")

        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise CustomException("Error during pipeline initialization", e)

    def recommend(self, query: str) -> str:
        try:
            logger.info(f"Received user recommendation query: '{query}'")

            # 3. Executes our clean, manual RAG process
            recommendation = self.recommender.get_recommendation(query)

            logger.info("Recommendation generated successfully...")
            return recommendation

        except Exception as e:
            logger.error(f"Failed to get recommendation: {str(e)}")
            raise CustomException(
                "Error during generation step of recommendation pipeline", e
            )
