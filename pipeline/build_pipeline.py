import os
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting to build pipeline...")

        # 1. FIXED: Explicitly guarantee the directory structure exists for the output file
        os.makedirs("data", exist_ok=True)

        loader = AnimeDataLoader(
            "data/anime_with_synopsis.csv", "data/anime_updated.csv"
        )
        processed_csv = loader.load_and_process()

        logger.info("Data loaded and processed successfully...")

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()

        # 2. FIXED: Corrected minor typos in the log strings
        logger.info("Vector store built successfully...")
        logger.info("Pipeline execution built successfully...")

    except Exception as e:
        logger.error(f"Failed to execute pipeline: {str(e)}")
        raise CustomException("Error encountered during pipeline execution", e)


if __name__ == "__main__":
    main()
