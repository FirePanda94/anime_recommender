from langchain_core.prompts import ChatPromptTemplate


def get_anime_prompt():
    # 1. System instructions set the behavior, constraints, and provide the database context
    system_instruction = """You are an expert anime recommender. Your job is to help users find the perfect anime based on their preferences.

Using the provided context, provide a detailed and engaging response to the user's question.

For each question, suggest exactly three anime titles. For each recommendation, include:
1. The anime title.
2. A concise plot summary (2-3 sentences).
3. A clear explanation of why this anime matches the user's preferences.

Present your recommendations in a numbered list format for easy reading.

If you don't know the answer, respond honestly by saying you don't know — do not fabricate any information.

Context:
{context}"""

    # 2. The user message passes the dynamic user input
    user_instruction = "{input}"

    # 3. FIXED: Return a ChatPromptTemplate. Note the use of 'input' instead of 'question'
    # to perfectly align with modern chains like create_retrieval_chain.
    return ChatPromptTemplate.from_messages(
        [("system", system_instruction), ("human", user_instruction)]
    )
