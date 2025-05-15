

from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_core.tools import tool

# Set up the wrapper
wrapper = ArxivAPIWrapper(max_results=3)  # Limit to 3 papers for brevity

# Create the LangChain Tool
search = ArxivQueryRun(api_wrapper=wrapper)

@tool
def arxiv_search(query: str) -> str:
    """
    Search arXiv for academic papers related to the query.
    Returns titles and summaries of the top results.
    """
    result = search.invoke(query)
    return result
