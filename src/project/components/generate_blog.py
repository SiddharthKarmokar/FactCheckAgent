from src.project.components.agents import blog_writer
from src.project.components.logging import logger
from deep_translator import GoogleTranslator
from src.project.components.config import INDIAN_LANGUAGES

def generate_blog(summary, topic, sources, language="en"):
    logger.info(f"Generating fact-checked blog for topic: {topic}")

    try:
        blog_prompt = (
            f"Write a detailed, well-structured fact-checking blog on '{topic}' using the following summary:\n\n"
            f"{summary}\n\nSources:\n{sources}\n\n"
            "Cross-check facts and highlight inconsistencies. Provide an objective credibility score for each source."
            "Ensure the blog has an engaging introduction, key takeaways, and a strong conclusion."
            "Include a section listing the sources used for verification."
            "Make sure that the conclusion properly illustrates the sentiment, if fact-check is creadible or not"
        )
        response = blog_writer.run(blog_prompt)
        blog_content = getattr(response, "content", str(response))

        if language in INDIAN_LANGUAGES:
            blog_content = GoogleTranslator(source="auto", target=language).translate(blog_content)
            logger.info(f"Translated blog content to {language}")

        logger.info("Blog successfully generated")
        return blog_content
    except Exception as e:
        logger.error(f"Error generating blog: {e}", exc_info=True)
        return "Failed to generate blog."
