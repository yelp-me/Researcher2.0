from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.tools import tool
from duckduckgo_search.exceptions import DuckDuckGoSearchException

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    search = DuckDuckGoSearchRun()
    try:
        result = search.run(query)
        return result
    except DuckDuckGoSearchException:
        return "Web search rate limit hit. Try again later or slow down the requests."
    except Exception as e:
        return f"Web search failed: {str(e)}"
