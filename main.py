import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType

from tools.pdf_search import pdf_search
from tools.web_search import web_search
from tools.arxiv_search import arxiv_search
from tools.wikipedia_search import wikipedia_search

# load .env
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# load prompt for agent
def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

system_prompt = load_prompt()

# setup LLM + agent
llm = ChatGroq(model_name="llama3-8b-8192")

agent = initialize_agent(
    tools=[pdf_search, web_search, arxiv_search, wikipedia_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_prompt},
)

# page config
st.set_page_config(page_title="CoreSearch", layout="wide")

# custom styles
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f1f1f1;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent;
    }

    .chat-bubble {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 15px;
        line-height: 1.6;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .user-bubble {
        background-color: #3a3f5c;
        color: #e0e0e0;
        text-align: right;
    }

    .assistant-bubble {
        background-color: #1f2937;
        color: #f8f8f8;
        text-align: left;
    }

    .stTextInput > div > input,
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.07);
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 8px;
    }

    input[type="file"] {
        padding: 4px;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# app title
st.title("CoreSearch — Gen AI Research Assistant")

# PDF upload
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("./uploads", exist_ok=True)
    with open("./uploads/latest.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.toast("✅ PDF uploaded and ready.")

# input + response
query = st.text_input("💬 Message", placeholder="Type your message and press Enter...")

if query.strip() != "":
    st.markdown(f"<div class='chat-bubble user-bubble'>{query}</div>", unsafe_allow_html=True)

    with st.spinner("CoreSearch is thinking..."):
        response = agent.run(query)

    st.markdown(f"<div class='chat-bubble assistant-bubble'>{response}</div>", unsafe_allow_html=True)

    st.stop()
