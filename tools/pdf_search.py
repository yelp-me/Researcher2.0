from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools import tool
import os
import uuid

@tool
def pdf_search(query: str) -> str:
    """Search the last uploaded PDF file for information related to the query."""
    try:
        latest_pdf = "./uploads/latest.pdf"  # Always overwrite this one
        if not os.path.exists(latest_pdf):
            return "No PDF uploaded yet."

        loader = PyPDFLoader(latest_pdf)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        embeddings = OllamaEmbeddings(model="moondream")
        vectorstore = Chroma.from_documents(
            splits,
            embeddings,
            persist_directory=f"./chroma_store/{uuid.uuid4().hex}"
        )

        retriever = vectorstore.as_retriever()
        results = retriever.invoke(query)

        if not results:
            return "No relevant info found in the uploaded PDF."

        return "\n\n".join([doc.page_content for doc in results[:2]])
    except Exception as e:
        return f"PDF search failed: {str(e)}"
