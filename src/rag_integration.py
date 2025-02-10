import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from groq import Groq
from data_extraction import parse_chat

embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

def build_vector_store_with_chroma(chat_file) -> Chroma:
    df = parse_chat(chat_file)
    texts = df["message"].tolist()
    from chromadb.config import Settings
    client_settings = Settings(persist_directory="./chroma_db")
    collection_name = "whatsapp_chat"
    try:
        existing_store = Chroma(collection_name=collection_name, client_settings=client_settings)
        existing_store.delete_collection()
    except Exception:
        pass
    vector_store = Chroma.from_texts(texts, embedding=embeddings, collection_name=collection_name, client_settings=client_settings)
    return vector_store

def rag_generate_answer(query: str, vector_store: Chroma) -> str:
    retrieved_docs = vector_store.similarity_search(query, k=3)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = f"""You are a knowledgeable assistant. Your answer must be formatted as a markdown table with exactly three columns: Date, Time, and Message.
Extract the relevant details from the following chat context.
- **Date:** in YYYY-MM-DD format extracted from the chat timestamp.
- **Time:** in HH:MM format.
- **Message:** the actual chat message text.

Do not include any additional commentary or text. Output only the table in markdown.

Context:
{context}

Question: {query}
Answer (markdown table):"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content
