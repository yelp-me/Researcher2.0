from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

@tool
def pdf_search(query: str) -> str:
    """Search local PDFs for relevant information related to the query."""
    loader = PyPDFLoader("./pdf/sample.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        splits,
        embeddings,
        persist_directory="./chroma_store"
    )

    retriever = vectorstore.as_retriever()
    results = retriever.invoke(query)

    if not results:
        return "No relevant info found in the PDF."

    return results
