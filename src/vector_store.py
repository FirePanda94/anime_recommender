from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()


class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_dir: str = "chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vectorstore(self):
        loader = CSVLoader(
            file_path=self.csv_path, encoding="utf-8", content_columns="combined_info"
        )

        data = loader.load()
        db = Chroma.from_documents(
            documents=data, embedding=self.embedding, persist_directory=self.persist_dir
        )
        print(
            f"✅ Vector database successfully built and stored at '{self.persist_dir}'"
        )
        return db

    def load_vector_store(self):
        return Chroma(
            persist_directory=self.persist_dir, embedding_function=self.embedding
        )
