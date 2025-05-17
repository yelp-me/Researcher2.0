# 🧠 CoreSearch — Gen AI Research Assistant

CoreSearch is a lightweight AI research assistant powered by **Groq (LLaMA 3)** and **LangChain**. It lets you upload PDFs, ask questions, and pull in answers from multiple sources like the web, Wikipedia, and arXiv — all from a clean Streamlit interface.

No bloat. No memory. Just straight answers.

---

## 🚀 Features

- 🔍 **Ask questions about any PDF**  
  Uses embeddings + vector search (Chroma + Ollama) to pull relevant chunks and feed them to the LLM.

- 🌐 **Live Web Search**  
  Uses DuckDuckGo to pull recent info and news.

- 📚 **arXiv Search**  
  Find academic papers related to your query and summarize them.

- 📖 **Wikipedia Lookup**  
  Quick summaries from Wikipedia for background context.

- ⚡ **Fast LLM Backend**  
  Powered by **Groq-hosted LLaMA 3**, giving near-instant answers.

---

## 🛠 Tech Stack

| Tech         | Role                        |
|--------------|-----------------------------|
| Streamlit    | Frontend UI                 |
| LangChain    | Tool routing + agent logic  |
| Groq + LLaMA | Language model backend      |
| Chroma       | PDF vector DB               |
| Ollama       | Embedding model             |
| DuckDuckGo   | Web search results          |
| arXiv API    | Academic paper lookup       |
| Wikipedia API| Quick fact search           |

---

## 🧪 Local Setup

1. **Clone the repo**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
