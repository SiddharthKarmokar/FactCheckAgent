import streamlit as st
from src.project.components.fetch_news import fetch_news
from src.project.components.generate_blog import generate_blog
from src.project.components.generate_image import generate_image
from src.project.components.config import INDIAN_LANGUAGES, get_random_topic
from src.project.components.logging import logger
from src.project.components.confidence_score import calculate_confidence_score
from src.project.components.get_sources import get_sources  # Import the function

st.title("🔍 AI-Powered Fact-Checking")

topic = st.text_input("Enter a topic to fact-check")
language = st.selectbox("Select language", ["en"] + INDIAN_LANGUAGES)

if st.button("Fact-Check"):
    logger.info("Fact-checking process started")

    if not topic:
        st.write("### Selecting a random region and topic...")
        city, topic = get_random_topic()

    logger.info(f"Topic: {topic}")
    st.success(f"Topic: {topic}")

    st.write("### Selecting relevant sources...")
    selected_sources = get_sources(topic)
    st.write("### 📡 Selected News Sources")
    st.write("#### We've identified the best sources for this topic:")
    for source, score in selected_sources.items():
        st.write(f"- **{source}** (Relevance Score: {score}/10)")
    
    # if st.button("Generate"):
    st.write("### Fetching news and verifying sources...")
    news_summary, sources = fetch_news(topic, language, selected_sources)
    st.success("News Retrieved and Verified!")

    st.write("### Generating fact-checked blog post...")
    blog_content = generate_blog(news_summary, topic, sources, language)

    st.write("## 📝 Fact-Checked Summary")
    st.markdown(blog_content, unsafe_allow_html=True)

    st.write("### Calculating Confidence Score...")
    confidence_score = calculate_confidence_score(sources, news_summary)
    st.progress(confidence_score)
    st.write(f"**Confidence Score:** {confidence_score:.2f} (Scale: 0-1)")

    st.write("### Generating image for visualization...")
    image_url = generate_image(topic)
    st.image(image_url, caption="Generated Image")

    logger.info("Fact-checking blog generation completed")
