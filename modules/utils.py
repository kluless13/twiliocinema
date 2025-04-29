"""Utility functions for the WhatsApp Cinema Bot"""
import sys
import json
from loguru import logger

def setup_logging():
    """Configure logging for the application"""
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 week",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

def load_movie_data(filename="data/movies.json"):
    """Load movie data from JSON file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load movie data: {str(e)}")
        return []

def safe_get(data, key, default=None):
    """Safely get a value from a dictionary"""
    try:
        return data.get(key, default)
    except:
        return default 