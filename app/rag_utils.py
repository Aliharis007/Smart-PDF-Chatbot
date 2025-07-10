from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from app.groq_setup import get_groq_llm
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to create FAISS vectorstore from documents
def create_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


# Function to set up RetrievalQA chain
def get_qa_chain(vectorstore):
    llm = get_groq_llm()
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain


# Function to summarize multiple documents in chunks to avoid token overflow
# Function to summarize multiple documents in chunks to avoid token overflow
def get_summary_chain(documents):
    llm = get_groq_llm()

    # Prompt for summarization
    summary_prompt = PromptTemplate.from_template(
        "Summarize the following text:\n\n{text}\n\nSummary:"
    )

    llm_chain = LLMChain(llm=llm, prompt=summary_prompt)
    summarize_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="text"
    )

    # Split documents into smaller chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = []
    for doc in documents:
        splits = text_splitter.split_documents([doc])
        chunks.extend(splits)

    # Batch summarization
    final_summary = ""
    batch_size = 3  # smaller batch to stay within token limits

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        try:
            summary = summarize_chain.run(batch)
            final_summary += f"\n\n{summary}"
        except Exception as e:
            print(f"Error summarizing batch {i}-{i + batch_size}: {e}")
            continue

    return final_summary.strip()

