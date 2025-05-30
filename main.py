import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from tools.pdf_search import pdf_search
from tools.web_search import web_search
from tools.arxiv_search import arxiv_search
from tools.wikipedia_search import wikipedia_search

# Set up Streamlit page
st.set_page_config(page_title="CoreSearch", page_icon="🧠", layout="wide")

# Branding
st.markdown("""
    <style>
        .big-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0;
        }
        .sub-text {
            color: #6c757d;
            font-size: 1rem;
            margin-top: 0;
        }
        .clear-button {
            text-align: right;
            margin-top: -30px;
        }
    </style>
    <div class='big-title'>🧠 CoreSearch</div>
    <div class='sub-text'>Ask smart questions. Get real answers. Powered by LLMs and live data.</div>
    <hr>
""", unsafe_allow_html=True)

# API Key from Streamlit secrets
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.stop()
    raise ValueError("Missing GROQ_API_KEY in Streamlit secrets.")

# Load system prompt
def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

system_prompt = load_prompt()

# Setup model & tools
llm = ChatGroq(model_name="mistral-saba-24b")
tools = [pdf_search, web_search, arxiv_search, wikipedia_search]
agent = create_react_agent(llm, tools)

# Session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Upload block
uploaded_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])
if uploaded_file:
    os.makedirs("./uploads", exist_ok=True)
    with open("./uploads/latest.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.success("PDF uploaded. You can now ask questions about it.")
else:
    st.markdown("_No PDF uploaded. You can still ask general questions._")

# Display past chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**CoreSearch:** {msg}")

# Input box
user_input = st.chat_input("Ask something about the PDF, web, arXiv, or Wikipedia...")

if user_input:
    st.chat_message("user").markdown(f"**You:** {user_input}")
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            answer = response["messages"][-1].content
            st.markdown(f"**CoreSearch:** {answer}")

            tool_messages = [
                msg for msg in response["messages"]
                if msg.type in ("tool", "function")
            ]

            if tool_messages:
                with st.expander("🧠 Agent Tool Usage", expanded=False):
                    for i, msg in enumerate(tool_messages, 1):
                        role = msg.type
                        name = getattr(msg, "name", "unknown_tool")
                        content = msg.content
                        st.markdown(f"""
---
**Step {i}**  
- Role: `{role}`  
- Tool: `{name}`  
- Content: `{content}`
""")

    st.session_state.chat_history.append(("assistant", answer))
