import os
from dotenv import load_dotenv
import random

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN")
REDDIT_CLIENT_ID=os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET=os.getenv("REDDIT_CLIENT_SECRET")
NASA_API_KEY=os.getenv("NASA_API_KEY")
INDIAN_NEWS_API_KEY=os.getenv("INDIAN_NEWS_API_KEY")
FACT_CHECKING_API_KEY=os.getenv("FACT_CHECKING_API_KEY")
DEFAULT_LANGUAGE=os.getenv("DEFAULT_LANGUAGE")

INDIAN_LANGUAGES = ["hi", "bn", "te", "mr", "ta", "ur", "gu", "kn", "ml", "pa", "en"]

CITIES_AND_TOPICS = {
    "Mumbai": "Stock Market Trends",
    "Bangalore": "Tech Startups Growth",
    "Hyderabad": "AI & Machine Learning Innovations",
    "Chennai": "Cyclone Preparedness & Impact",
    "Kolkata": "Heritage Preservation Challenges",
    "Pune": "EV Adoption in India",
    "Jaipur": "Tourism & Cultural Festivals",
    "Ahmedabad": "Smart City Developments",
    "Lucknow": "Food & Street Cuisine Culture",
    "Delhi": "Crime in the city",
}

def get_random_topic():
    return random.choice(list(CITIES_AND_TOPICS.items()))
