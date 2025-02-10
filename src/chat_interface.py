# chat_interface.py
import streamlit as st
from rag_integration import build_vector_store_with_chroma, rag_generate_answer

st.sidebar.title("Settings")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat Export (.txt)", type="txt")
vector_store = None

if uploaded_file:
    # Build (or rebuild) the vector store from the uploaded chat file.
    vector_store = build_vector_store_with_chroma(uploaded_file)
    st.success("Chat data vectorized and stored!")
else:
    st.sidebar.warning("Please upload a chat file to get started.")

st.title("RAG Chat Interface with Groq LLM Integration")
user_input = st.text_input("Enter your prompt:")

if st.button("Send"):
    if not uploaded_file:
        st.error("Please upload your chat file first!")
    elif not user_input.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating answer..."):
            response = rag_generate_answer(user_input, vector_store)
        st.markdown("### Response:")
        st.write(response)
