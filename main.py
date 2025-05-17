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

# Set API key
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# Load system instructions
def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

system_prompt = load_prompt()

# Define model and tools
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

# Set up logic agent
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
st.title("CoreSearch — Document and Web Researcher")

# Chat state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    os.makedirs("./uploads", exist_ok=True)
    with open("./uploads/latest.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.toast("PDF uploaded and ready.")

# Show previous messages
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Input
user_input = st.chat_input("Ask something about the PDF or search the web...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Working on it..."):
            response = agent_executor.invoke({
                "input": user_input,
                "agent_scratchpad": format_log_to_messages([]),
            })
            answer = response["output"]
            st.markdown(answer)

    st.session_state.chat_history.append(("assistant", answer))
