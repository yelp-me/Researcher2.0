# tools/wikipedia_tool.py

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool

# Setup wrapper
wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)

# LangChain tool setup
search = WikipediaQueryRun(api_wrapper=wrapper)

@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia using LangChain wrapper and return a short summary.
    """
    result = search.invoke(query)
    return result
