from src.project.components.agents import source_selector
from src.project.components.logging import logger
import json

AVAILABLE_SOURCES = {"duckduckgo", "x", "reddit", "arxiv", "nasa", "indian_sources"}

def get_sources(topic: str):
    """
    Determines the most relevant sources for the given topic.
    Returns a dictionary of sources with relevance scores (0-10).
    Sources with very low scores or unavailable sources are removed.
    """
    response = source_selector.run(f"Determine the best sources for the topic: {topic}. Only consider these sources: {', '.join(AVAILABLE_SOURCES)}.  Output only a JSON object without explanations or additional text, formatted as: {{'sources': {{'source_name': relevance_score}}}} make sure to not alter the source_name from the given")
    try:
        response_text = response.content if hasattr(response, "content") else str(response)
        logger.info(response_text)
        sources = json.loads(response_text)
        
        if 'sources' in sources:
            sources = sources["sources"]
        if sources:
            sources = {key: value for key, value in sources.items() if value > 2}
            logger.info(f"Relevant Sources: {sources}")
            return sources
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Error decoding JSON: {e}")
        return {}
    
    return {}


