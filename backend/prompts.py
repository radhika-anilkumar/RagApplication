from langchain.prompts import ChatPromptTemplate

SYSTEM_PROMPT: str = (
    "You are a helpful assistant. "
    "Answer using only the provided context. "
    "If the answer isn’t in the context, say you don’t know. "
    "Cite sources as [number] that match the provided sources list."
)

ANSWER_PROMPT: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        "Question: {question}\n\n"
        "Context:\n{context}\n\n"
        "Provide a concise answer first, then bullet citations."
    ),
])
