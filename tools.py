from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun,WikipediaQueryRun
from langchain.tools import Tool
from datetime import datetime
import os
from langchain.tools import Tool
from datetime import datetime

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

wiki_api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
def wiki_func(query: str) -> str:
    return wiki_api.run(query)   # ✅ safe callable

wiki_tool = Tool(
    name="wikipedia",
    func=wiki_func,
    description="Fetch summaries from Wikipedia"
)

TOOLS = [search_tool, wiki_tool]