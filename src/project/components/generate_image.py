from src.project.components.logging import logger

def generate_image(prompt):
    logger.info(f"Generating image for prompt: {prompt}")

    try:
        image_url = f"https://image.pollinations.ai/prompt/{prompt}"
        logger.info(f"Image successfully generated: {image_url}")
        return image_url
    except Exception as e:
        logger.error(f"Error generating image: {e}", exc_info=True)
        return None
