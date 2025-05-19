import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

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
            font-size: 2.4rem;
            font-weight: 600;
            margin-bottom: 0;
        }
        .sub-text {
            color: gray;
            font-size: 0.95rem;
            margin-top: 0;
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

prompt = ChatPromptTemplate.from_template(system_prompt)


agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

# Session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload block
uploaded_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])
if uploaded_file:
    os.makedirs("./uploads", exist_ok=True)
    with open("./uploads/latest.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.success("PDF uploaded. You can now ask questions about it.")
else:
    st.info("Upload a PDF to enable document-based search.")

# Display past chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Input box
user_input = st.chat_input("Ask something about the PDF, web, arXiv, or Wikipedia...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor.invoke({"input": user_input})
            answer = response["output"]
            st.markdown(f"**Answer:**\n\n{answer}")

            if "intermediate_steps" in response:
                with st.expander("🧠 Agent Thought Process", expanded=False):
                    for i, (action, observation) in enumerate(response["intermediate_steps"], 1):
                        st.markdown(f"""
**Step {i}**
- Thought: {action.log.strip()}
- Action: `{action.tool}`
- Input: `{action.tool_input}`
- Observation: {observation}
""")

    st.session_state.chat_history.append(("assistant", answer))
