from src.project.components.logging import logger

def calculate_confidence_score(news_sources, fact_check_analysis):
    """
    Calculate a confidence score for the fact-checking process based on:
    - Number of credible sources
    - Consistency across sources
    - AI confidence in fact-checking analysis
    """
    try:
        if not news_sources:
            logger.warning("No sources provided. Confidence score will be low.")
            return 0.2  # Minimum confidence score

        credibility_scores = {
            "government": 0.9,
            "reputed_news": 0.8,
            "scientific_paper": 0.95,
            "social_media": 0.4,
            "unknown": 0.3
        }

        total_score = 0
        for source in news_sources:
            source_type = classify_source(source)
            total_score += credibility_scores.get(source_type, 0.3)

        avg_source_score = total_score / len(news_sources)
        consistency_score = analyze_consistency(fact_check_analysis)
        final_score = (avg_source_score * 0.6) + (consistency_score * 0.4)

        logger.info(f"Calculated confidence score: {final_score:.2f}")
        return round(final_score, 2)
    except Exception as e:
        logger.error(f"Error calculating confidence score: {e}", exc_info=True)
        return 0.5  


def classify_source(source_url):
    """Classify the type of source based on URL or metadata."""
    if "gov" in source_url or "nasa" in source_url:
        return "government"
    elif "bbc" in source_url or "reuters" in source_url or "thehindu" in source_url:
        return "reputed_news"
    elif "arxiv" in source_url or "researchgate" in source_url:
        return "scientific_paper"
    elif "twitter.com" in source_url or "reddit.com" in source_url:
        return "social_media"
    else:
        return "unknown"


def analyze_consistency(fact_check_analysis):
    """Analyze how consistent the information is across different sources."""
    if "high consistency" in fact_check_analysis:
        return 0.9
    elif "moderate consistency" in fact_check_analysis:
        return 0.7
    elif "low consistency" in fact_check_analysis:
        return 0.4
    else:
        return 0.5  # Default neutral score
