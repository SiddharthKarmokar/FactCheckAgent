import os
import requests
from src.project.components.agents import news_agent
from src.project.components.logging import logger
from deep_translator import GoogleTranslator
from src.project.components.config import (
    INDIAN_LANGUAGES, TWITTER_BEARER_TOKEN, REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET, NASA_API_KEY, INDIAN_NEWS_API_KEY
)

def fetch_news_from_duckduckgo(topic):
    response = news_agent.run(f"Find the latest news articles about {topic} and summarize them. Include sources.")
    
    if isinstance(response, list):
        response = " ".join(str(res) for res in response)
    
    return str(response)

def fetch_news_from_x(topic):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={topic}&tweet.fields=text,source"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers).json()
        tweets = [tweet["text"] for tweet in response.get("data", [])]
        return "\n".join(tweets) if tweets else "No recent tweets found."
    except Exception as e:
        logger.error(f"Error fetching news from X: {e}")
        return ""

def fetch_news_from_reddit(topic):
    url = f"https://www.reddit.com/r/news/search.json?q={topic}&sort=new"
    headers = {"User-Agent": "news-agent-bot"}
    
    try:
        response = requests.get(url, headers=headers).json()
        posts = [post["data"]["title"] for post in response.get("data", {}).get("children", [])]
        return "\n".join(posts) if posts else "No relevant Reddit posts found."
    except Exception as e:
        logger.error(f"Error fetching news from Reddit: {e}")
        return ""

def fetch_news_from_arxiv(topic):
    url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results=5"
    
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "No relevant research papers found."
    except Exception as e:
        logger.error(f"Error fetching news from Arxiv: {e}")
        return ""

def fetch_news_from_nasa(topic):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    
    try:
        response = requests.get(url).json()
        return response.get("explanation", "No NASA news available.")
    except Exception as e:
        logger.error(f"Error fetching news from NASA: {e}")
        return ""

def fetch_news_from_indian_sources(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={INDIAN_NEWS_API_KEY}"
    
    try:
        response = requests.get(url).json()
        articles = [article["title"] + " - " + article["url"] for article in response.get("articles", [])]
        return "\n".join(articles) if articles else "No relevant Indian news found."
    except Exception as e:
        logger.error(f"Error fetching Indian news: {e}")
        return ""

def fetch_news(topic, language="en", sources=None):
    logger.info(f"Fetching news for topic: {topic} in language: {language}")

    available_sources = {
        "duckduckgo": fetch_news_from_duckduckgo,
        "x": fetch_news_from_x,
        "reddit": fetch_news_from_reddit,
        "arxiv": fetch_news_from_arxiv,
        "nasa": fetch_news_from_nasa,
        "indian_sources": fetch_news_from_indian_sources
    }

    if not sources:
        logger.warning("No sources provided, defaulting to all.")
        sources = {key: 10 for key in available_sources}  # Use all sources with max score

    selected_sources = {k: v for k, v in available_sources.items() if k in sources}

    fetched_news = [func(topic) for func in selected_sources.values()]
    news_content = "\n\n".join(filter(None, fetched_news))

    if not news_content.strip():
        logger.error("No news found from selected sources.")
        return "No relevant news found."

    if language in INDIAN_LANGUAGES:
        try:
            news_content = GoogleTranslator(source="auto", target="en").translate(news_content)
            logger.info("Translated news content to English.")
        except Exception as e:
            logger.error(f"Error translating news: {e}")

    logger.info("Successfully fetched and processed news")
    return news_content, selected_sources
