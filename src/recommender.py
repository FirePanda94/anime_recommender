import os
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ==========================================
# SETUP DEDICATED RETRIEVAL LOGGER
# ==========================================
os.makedirs("logs", exist_ok=True)
retrieval_logger = logging.getLogger("retrieval_logger")
retrieval_logger.setLevel(logging.INFO)
retrieval_logger.propagate = False

file_handler = logging.FileHandler("logs/retrieval.log", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s -\n%(message)s\n" + "=" * 80 + "\n"
)
file_handler.setFormatter(formatter)
retrieval_logger.addHandler(file_handler)

# ==========================================
# ANIME SYSTEM PROMPT TEMPLATE
# ==========================================
SYSTEM_PROMPT_TEMPLATE = """You are an expert anime recommender. Your job is to help users find the perfect anime based on their preferences.

MANDATORY RULES:
1. STRICT CONTEXT USE: Suggest anime titles found ONLY in the provided context below. Do not use outside knowledge or extrapolate details.
2. ANSWER DIRECTLY: Start listing the recommendations immediately. Do not include introductory fluff (e.g., "Based on your choices..."). 
3. STRUCTURE FOR EACH ENTRY:
   - The anime title.
   - A concise plot summary (2-3 sentences).
   - A clear explanation of why this anime matches the user's preferences based strictly on the text.
4. PRESENTATION: Present your recommendations in a numbered list format for easy reading.
5. FALLBACK: If the context contains zero relevant information, reply exactly: "I don't have enough information in the provided database to answer this."

CONTEXT:
{context}"""


class AnimeRecommender:
    def __init__(self, vector_store, api_key: str = None, model_name: str = None):
        self.vector_store = vector_store

        # Setup local LM Studio connection
        self.llm = ChatOpenAI(
            base_url="http://localhost:1234/v1",
            api_key="not-needed",
            model="qwen2.5-7b-instruct",
            temperature=0.0,
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def format_context(self, docs: list) -> str:
        if not docs:
            return "No anime context retrieved."

        blocks = []
        for i, doc in enumerate(docs, 1):
            # Since you skipped separate metadata, everything is in page_content
            blocks.append(f"[Anime Entry #{i}]\n{doc.page_content.strip()}")
        return "\n\n---\n\n".join(blocks)

    def get_recommendation(self, query: str) -> str:
        # STEP 1: Fetch matching documents from the vector database
        matching_docs = self.retriever.invoke(query)

        # Write to your isolated log file
        log_payload = f"USER QUERY: {query}\n\n"
        for idx, doc in enumerate(matching_docs, 1):
            log_payload += f"--- RETRIEVED MATCH #{idx} ---\n{doc.page_content}\n\n"
        retrieval_logger.info(log_payload.strip())

        if not matching_docs:
            return "I don't have enough information in the provided database to answer this."

        # STEP 2: Format text context block explicitly
        context_str = self.format_context(matching_docs)

        # STEP 3: Build explicit system prompt using the template matrix
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context_str)

        # STEP 4: Call the local LLM using explicit message objects
        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query),
            ]
        )

        return response.content
