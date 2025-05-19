from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.tools import tool
import os
import streamlit as st

@tool
def pdf_search(query: str) -> str:
    """Search the last uploaded PDF file for information related to the query."""
    try:
        latest_pdf = "./uploads/latest.pdf"
        if not os.path.exists(latest_pdf):
            return "No PDF uploaded yet."

        loader = PyPDFLoader(latest_pdf)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=st.secrets["HUGGINGFACEHUB_API_TOKEN"],
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever()
        results = retriever.get_relevant_documents(query)

        if not results:
            return "No relevant info found in the uploaded PDF."

        return "\n\n".join([doc.page_content for doc in results[:2]])

    except Exception as e:
        return f"PDF search failed: {str(e)}"
