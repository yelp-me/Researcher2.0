# 🧠 CoreSearch — Gen AI Research Assistant

CoreSearch is a lightweight AI research assistant powered by Groq (Mistral SABA 24B) and LangChain. It lets you upload PDFs, ask questions, and pull in answers from multiple sources like the web, Wikipedia, and arXiv — all from a clean Streamlit interface.

No bloat. No memory. Just straight answers.

---

## 🚀 Features

- 🔍 **Ask questions about any PDF**  
  Uses LangChain + Chroma + Ollama-style embeddings to search your uploaded docs.

- 🌐 **Live Web Search**  
  Pulls real-time info using DuckDuckGo.

- 📚 **arXiv Search**  
  Finds relevant academic papers via the arXiv API.

- 📖 **Wikipedia Lookup**  
  Gets quick, high-level summaries and facts.

- ⚡ **Fast LLM Backend**  
  Powered by Groq-hosted `mistral-saba-24b` — one of the fastest available LLMs.

- 🎨 **Modern UI**  
  Minimalist Streamlit chat interface with a custom dark theme.

- 🔧 **No Tool Overuse**  
  Uses the ReAct agent framework to make smart tool choices — only one per query.

---

## 🛠 Tech Stack

| Tech               | Role                         |
|--------------------|------------------------------|
| **Streamlit**      | Frontend UI                  |
| **LangChain**      | Agent + tool logic           |
| **Groq + Mistral** | LLM backend (mistral-saba-24b) |
| **Chroma**         | PDF vector DB                |
| **OllamaEmbeddings** | Text embedding model      |
| **DuckDuckGo**     | Web search                   |
| **arXiv API**      | Academic paper lookup        |
| **Wikipedia API**  | Quick fact search            |

---

## 🧪 Local Setup

### ✅ Step 1: Clone the Repo

```bash
git clone https://github.com/your-username/coresearch
cd coresearch


## ✅ Step 2: Create a Virtual Environment

To isolate your project dependencies, set up a virtual environment.

### 🔧 Create and Activate:

```bash
python -m venv venv

### 📁 `STEP_3_INSTALL_REQUIREMENTS.md`

```markdown
# ✅ Step 3: Install Dependencies

Install all Python libraries needed for CoreSearch.

```bash
pip install -r requirements.txt


### 📁 `STEP_4_ENV_FILE.md`

```markdown
# ✅ Step 4: Add API Key

Create a `.env` file in your project root and paste your **Groq API key**:


Get a free API key from 👉 https://console.groq.com

> This is used to authenticate your app with Groq’s LLM infrastructure.

Make sure `.env` is in your `.gitignore` so it doesn't get pushed to GitHub.

# ✅ Step 5: Run the App

Start the Streamlit server:

```bash
streamlit run main.py


---

### 📁 `STEP_6_FOLDER_LAYOUT.md`

```markdown
# ✅ Step 6: Folder Layout Overview

Here’s what your project structure should look like:

coresearch/
├── main.py # Streamlit app + agent logic
├── prompts/
│ └── agent_prompt.txt # System prompt
├── tools/
│ ├── pdf_search.py
│ ├── web_search.py
│ ├── arxiv_search.py
│ └── wikipedia_search.py
├── uploads/
│ └── latest.pdf # Most recent uploaded PDF
├── .env # Your Groq API key
├── .gitignore # Ignore .env, venv, etc.
└── requirements.txt # Python packages