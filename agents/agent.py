

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from tools.pdf_search import pdf_search
from tools.web_search import web_search
from tools.arxiv_search import arxiv_search
from tools.wikipedia_search import wikipedia_search




def load_prompt(path="prompts/agent_prompt.txt") -> str:
    with open(path, "r") as f:
        return f.read()

def build_agent():
    system_prompt = load_prompt()
    llm = ChatGroq(model_name="mixtral-8x7b-32768")

    return initialize_agent(
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
