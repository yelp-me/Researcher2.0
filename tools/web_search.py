from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool

wrapper = DuckDuckGoSearchAPIWrapper()

search = DuckDuckGoSearchRun(api_wrapper=wrapper)


@tool
def web_search(query: str) -> str:
    """
    Web search using duckduckgo.
    """
    result = search.invoke(query)
    
    return result