# main.py

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from tools import (
    pdf_search,
    web_search,
    arxiv_search,
    wikipedia_search,
   
)

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Load agent prompt
def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

system_prompt = load_prompt()

# Set up LLM
llm = ChatGroq(model_name="mixtral-8x7b-32768")

# Initialize agent
agent = initialize_agent(
    tools=[
        pdf_search,
        web_search,
        arxiv_search,
        wikipedia_search,
      
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_prompt}
)

# Streamlit UI
st.set_page_config(page_title="Research Assistant", layout="wide")
st.markdown(
    """
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .chat-bubble {
            padding: 10px 15px;
            margin: 8px 0;
            border-radius: 12px;
            font-size: 16px;
            line-height: 1.5;
        }
        .user-bubble {
            background-color: #cce4ff;
            color: #000000;
            text-align: right;
        }
        .assistant-bubble {
            background-color: #ffffff;
            color: #000000;
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧠 Research Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input("Ask me anything research-related...")

if query:
    with st.spinner("Thinking..."):
        response = agent.run(query)
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("assistant", response))

for role, message in st.session_state.chat_history:
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{message}</div>", unsafe_allow_html=True)
