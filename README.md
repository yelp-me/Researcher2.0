🧠 CoreSearch — Gen AI Research Assistant
CoreSearch is a lightweight AI research assistant powered by Groq (Mistral SABA 24B) and LangChain. Upload PDFs, ask questions, and pull answers from sources like the web, Wikipedia, and arXiv — all through a clean Streamlit interface.

No bloat. No memory. Just straight answers.

🚀 Features
🔍 Ask Questions About Any PDF
Uses LangChain + Chroma + Ollama-style embeddings to search your uploaded documents.

🌐 Live Web Search
Real-time info pulled via DuckDuckGo.

📚 arXiv Integration
Fetches academic papers using the arXiv API.

📖 Wikipedia Lookup
Quick summaries and factual answers from Wikipedia.

⚡ Fast LLM Backend
Powered by Groq-hosted mistral-saba-24b, one of the fastest open models available.

🎨 Clean, Dark-Themed UI
Minimalist interface built with Streamlit.

🔧 Smart Tool Use
Uses ReAct agent logic to avoid overusing tools — one per query.

🛠 Tech Stack
Tech	Purpose
Streamlit	Frontend UI
LangChain	Agent + tool orchestration
Groq + Mistral	LLM backend (mistral-saba-24b)
Chroma	Vector DB for PDF chunks
OllamaEmbeddings	Embedding model
DuckDuckGo	Web search tool
arXiv API	Research paper fetcher
Wikipedia API	Quick fact retriever

🧪 Local Setup
✅ Step 1: Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/coresearch
cd coresearch
✅ Step 2: Set Up a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
✅ Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
✅ Step 4: Add Your API Key
Create a .env file in the project root:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key_here
You can get a free key from: https://console.groq.com
Make sure .env is in your .gitignore.

✅ Step 5: Run the App
bash
Copy
Edit
streamlit run main.py
📁 Project Structure
bash
Copy
Edit
coresearch/
├── main.py                  # Streamlit app + agent logic
├── prompts/
│   └── agent_prompt.txt     # Custom system prompt
├── tools/
│   ├── pdf_search.py
│   ├── web_search.py
│   ├── arxiv_search.py
│   └── wikipedia_search.py
├── uploads/
│   └── latest.pdf           # Last uploaded PDF
├── .env                     # API key config (not checked in)
├── .gitignore               # Ignores .env, venv, etc.
└── requirements.txt         # Dependency list