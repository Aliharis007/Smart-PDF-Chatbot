# streamlit_app.py

import streamlit as st
from app.pdf_utils import load_pdf
from app.rag_utils import create_vectorstore, get_qa_chain, get_summary_chain

st.set_page_config(page_title="📚 Smart PDF Chatbot", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Chat with your PDFs using AI 🚀</h1>", unsafe_allow_html=True)
st.markdown("---")

uploaded_files = st.file_uploader("📂 Upload one or more PDF files", type="pdf", accept_multiple_files=True)

chat_mode = st.radio("🧠 Select Mode", ["Chat with PDF", "Summarize PDF"])

if uploaded_files:
    with st.spinner("⏳ Reading and processing..."):
        all_docs = []
        for file in uploaded_files:
            docs = load_pdf(file)
            all_docs.extend(docs)
        vectorstore = create_vectorstore(all_docs)

    if chat_mode == "Chat with PDF":
        query = st.text_input("💬 Ask a question about the PDF(s)")
        if query:
            with st.spinner("🔍 Finding answer..."):
                qa_chain = get_qa_chain(vectorstore)
                result = qa_chain.run(query)
                st.success(result)

    elif chat_mode == "Summarize PDF":
        if st.button("📝 Generate Summary"):
            with st.spinner("🧠 Summarizing content..."):
                summary = get_summary_chain(all_docs)
                st.info(summary)
