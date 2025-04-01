from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.storage.agent.postgres import PgAgentStorage
from phi.model.ollama import Ollama 
from src.project.components.config import POSTGRES_URL

news_storage = PgAgentStorage(table_name="news_agent", db_url=POSTGRES_URL)
blog_storage = PgAgentStorage(table_name="blog_writer", db_url=POSTGRES_URL)
source_storage = PgAgentStorage(table_name="source_selector", db_url=POSTGRES_URL)

source_selector = Agent(
    name="Source Selector",
    model=Ollama(id="llama3.2"),
    storage=source_storage,
    instructions=[
    "Analyze the given topic and determine the most relevant news sources.",
    "Rank each source from 0 to 10 based on relevance (0 = irrelevant, 10 = highly relevant).",
    "Provide a cleaned and ranked dictionary of the best sources for the given topic along with their relevance score.",
    "Consider only these sources:",
    "- 'duckduckgo': A privacy-focused search engine that aggregates news from multiple sources.",
    "- 'x': A microblogging platform (formerly Twitter) where real-time news and discussions take place.",
    "- 'reddit': A community-driven platform with various subreddits discussing trending news and opinions.",
    "- 'arxiv': A repository of scientific research papers, useful for academic and technical topics.",
    "- 'nasa': The official NASA website, a primary source for space and science-related news.",
    "- 'indian_sources': A collection of major Indian news portals providing localized news coverage."
    ],
    markdown=True,
)

news_agent = Agent(
    name="News Scraper",
    model=Ollama(id="llama3.2"),  
    tools=[DuckDuckGo(), ArxivToolkit()],  
    storage=news_storage,
    instructions=[
        "Fetch and summarize the latest news articles on a given topic from multiple sources.",
        "Use DuckDuckGo for general news and Arxiv for research papers if the topic is scientific.",
        "Include relevant source links for credibility.",
        "Summarize the content in a neutral and informative way, avoiding bias.",
    ],
    show_tool_calls=True,
    markdown=True,
)

blog_writer = Agent(
    name="Fact-Checking Blog Writer",
    model=Ollama(id="llama3.2"),
    storage=blog_storage,
    instructions=[
        "Write a well-structured fact-checked blog post on the given topic using the provided summary and sources.",
        "Cross-check facts using additional reliable sources when necessary.",
        "Ensure the blog includes an engaging introduction, key takeaways, and a strong conclusion.",
        "If contradictions arise between sources, highlight them and provide a reasoned conclusion.",
        "Include a section listing the sources of the news.",
    ],
    markdown=True,
)