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

# API key
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Load custom system prompt
def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

system_prompt = load_prompt()

# LLM and tools
llm = ChatGroq(model_name="mistral-saba-24b")
tools = [pdf_search, web_search, arxiv_search, wikipedia_search]

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

def format_log_to_messages(intermediate_steps):
    messages = []
    for action, observation in intermediate_steps:
        messages.append(AIMessage(content=action.log))
        messages.append(HumanMessage(content=f"Observation: {observation}"))
    return messages

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

# UI config
st.set_page_config(page_title="CoreSearch", layout="wide")
st.title("CoreSearch — Gen AI Research Assistant")

# Style updates
st.markdown("""
<style>
/* 🔧 Main background and text */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f0f0f !important;
    color: #f3f4f6 !important;
}

/* 🟣 Title */
h1 {
    color: #fafafa !important;
    font-weight: 700;
}

/* 💬 User bubble */
.stChatMessage.user .stMarkdown {
    background-color: #4c1d95 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    margin: 10px 0 10px auto !important;
    max-width: 75% !important;
    box-shadow: 0 0 8px rgba(0,0,0,0.35) !important;
}

/* 🧠 Assistant bubble */
.stChatMessage.assistant .stMarkdown {
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    margin: 10px auto 10px 0 !important;
    max-width: 75% !important;
    box-shadow: 0 0 8px rgba(0,0,0,0.35) !important;
}

/* ⌨️ Input box */
.stTextInput > div > input {
    background-color: #18181b !important;
    color: #f9fafb !important;
    border: 1px solid #3f3f46 !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

/* Extra input spacing */
[data-testid="stChatInput"] {
    padding-top: 24px !important;
}

/* 📂 Fix file uploader background + remove dashed border */
section[data-testid="stFileUploader"] {
    background-color: #1f1f22 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 20px !important;
    color: #f3f4f6 !important;
    box-shadow: 0 0 4px rgba(0,0,0,0.3) !important;
}

/* Hide file upload border */
section[data-testid="stFileUploader"] > div:first-child {
    border: none !important;
}

/* 🧼 Hide the default emoji icons */
.stChatMessageIcon {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)



# Init chat state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload box
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
if uploaded_file:
    os.makedirs("./uploads", exist_ok=True)
    with open("./uploads/latest.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.toast("✅ PDF uploaded and ready.")

# Show chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Input bar
user_input = st.chat_input("Type your question here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor.invoke({
                "input": user_input,
                "agent_scratchpad": format_log_to_messages([]),
            })
            answer = response["output"]
            st.markdown(answer)

    st.session_state.chat_history.append(("assistant", answer))
