# 🧠 CoreSearch — Research Assistant for Fast Answers

**CoreSearch** is a no-nonsense research assistant built with Groq (Mistral SABA 24B) and LangChain. Upload your PDFs, ask questions, and get relevant info from the web, Wikipedia, and arXiv — all inside a simple Streamlit app.

No chat history. No fluff. Just fast answers.

---

## 🚀 What It Does

- **Ask Questions About PDFs**  
  Index and search your uploaded documents using vector embeddings.

- **Live Web Search**  
  Pulls real-time info using DuckDuckGo.

- **arXiv Search**  
  Finds related academic papers using the arXiv API.

- **Wikipedia Lookup**  
  Quick summaries and facts from Wikipedia.

- **Fast Backend**  
  Runs on Groq-hosted `mistral-saba-24b`, one of the fastest open LLMs.

- **Simple UI**  
  Streamlit-powered dark interface. Clean and functional.

- **Smart Tool Use**  
  Uses ReAct agent logic to choose one tool per question — nothing extra.

---

## 🛠 Stack

| Tool/Library        | Purpose                     |
|---------------------|-----------------------------|
| Streamlit           | Web UI                      |
| LangChain           | Agent and tool control      |
| Groq + Mistral      | Language model backend      |
| Chroma              | Vector DB for PDFs          |
| OllamaEmbeddings    | Text embedding              |
| DuckDuckGo          | Real-time web search        |
| arXiv API           | Academic paper search       |
| Wikipedia API       | Quick fact retrieval        |

---

## 🧪 Getting Started (Local)

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/coresearch
cd coresearch
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your API Key

Create a `.env` file in the root of the project and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Grab your free key at: https://console.groq.com  
> Make sure `.env` is in your `.gitignore` file.

### 5. Run the App

```bash
streamlit run main.py
```

---

## 📁 Project Structure

```
coresearch/
├── main.py                  # Streamlit app + agent logic
├── prompts/
│   └── agent_prompt.txt     # System prompt for the agent
├── tools/
│   ├── pdf_search.py
│   ├── web_search.py
│   ├── arxiv_search.py
│   └── wikipedia_search.py
├── uploads/
│   └── latest.pdf           # Most recently uploaded PDF
├── .env                     # Your Groq API key
├── .gitignore               # Ignore .env, venv, etc.
└── requirements.txt         # Python dependencies
```

---

## 🔒 Note

CoreSearch does not store any data or chat history. It’s designed for fast, single-session research. Use it like a sharp tool — upload, ask, get out.

---

