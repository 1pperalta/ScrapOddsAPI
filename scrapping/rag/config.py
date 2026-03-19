"""
RAG System Configuration

Central configuration for the RAG (Retrieval-Augmented Generation) system.
Contains API keys, paths, league definitions, and model settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "scrapping" / "data"
LEAGUES_PATH = DATA_PATH / "leagues"
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"

# API Configuration
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
FOOTBALL_DATA_BASE_URL = "https://api.football-data.org/v4"

# Football-Data.org competition IDs
LEAGUES = {
    "Premier League": {
        "id": 2021,
        "code": "PL",
        "country": "England"
    },
    "La Liga": {
        "id": 2014,
        "code": "PD",
        "country": "Spain"
    },
    "Serie A": {
        "id": 2019,
        "code": "SA",
        "country": "Italy"
    },
    "Bundesliga": {
        "id": 2002,
        "code": "BL1",
        "country": "Germany"
    },
    "Ligue 1": {
        "id": 2015,
        "code": "FL1",
        "country": "France"
    },
    "Champions League": {
        "id": 2001,
        "code": "CL",
        "country": "Europe"
    }
}

# Embedding Configuration
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"
EMBEDDING_DIMENSION = 768
CHROMA_COLLECTION_NAME = "betting_context"

# Update Configuration
UPDATE_INTERVAL_HOURS = 24
MAX_RECENT_MATCHES = 5

# API Rate Limiting (Football-Data.org free tier: 10 requests/minute)
API_RATE_LIMIT_DELAY = 6  # seconds between requests

# Season Configuration
CURRENT_SEASON = "2024"

# Ensure directories exist
DATA_PATH.mkdir(parents=True, exist_ok=True)
LEAGUES_PATH.mkdir(parents=True, exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

