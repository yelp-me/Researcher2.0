from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.tools import tool
import os
import uuid
import streamlit as st

@tool
def pdf_search(query: str) -> str:
    """Search the last uploaded PDF file for information related to the query."""
    try:
        latest_pdf = "./uploads/latest.pdf"
        if not os.path.exists(latest_pdf):
            return "No PDF uploaded yet."

        # Load and split the PDF
        loader = PyPDFLoader(latest_pdf)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        # Use HuggingFace embeddings via their hosted API
        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=st.secrets["HUGGINGFACEHUB_API_TOKEN"],
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create a temporary vectorstore (or you can persist one for speed)
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=f"./chroma_store/{uuid.uuid4().hex}"
        )

        retriever = vectorstore.as_retriever()
        results = retriever.get_relevant_documents(query)

        if not results:
            return "No relevant info found in the uploaded PDF."

        return "\n\n".join([doc.page_content for doc in results[:2]])

    except Exception as e:
        return f"PDF search failed: {str(e)}"
