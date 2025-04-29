"""Cinema data and operations module"""
from loguru import logger
from typing import List, Dict, Optional, Any
from config import settings
from modules.utils import load_movie_data

class Movie:
    """Movie data model"""
    def __init__(self, movie_id: str, title: str, description: str = "", 
                 showtimes: List[str] = None,
                 special_show: bool = False,
                 location: str = None, 
                 duration: Optional[int] = None, 
                 price: Optional[float] = None, 
                 image_url: Optional[str] = None):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.showtimes = showtimes or []
        self.special_show = special_show
        self.location = location
        # Optional fields
        self.duration = duration
        self.price = price
        self.image_url = image_url

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Movie':
        """Create a Movie instance from dictionary data"""
        return cls(
            movie_id=data.get('id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            showtimes=data.get('showtimes', []),
            special_show=data.get('special_show', False),
            location=data.get('location', None),
            duration=data.get('duration'),
            price=data.get('price'),
            image_url=data.get('image_url')
        )

class CinemaService:
    """Service for managing cinema data and operations"""
    def __init__(self):
        self.movies = {}
        self.locations = settings.cinema.locations
        self.load_movies()
    
    def load_movies(self) -> None:
        """Load movie data from storage"""
        try:
            movie_data = load_movie_data()
            for movie_dict in movie_data:
                movie = Movie.from_dict(movie_dict)
                self.movies[movie.movie_id] = movie
            logger.info(f"Loaded {len(self.movies)} movies")
        except Exception as e:
            logger.error(f"Error loading movies: {str(e)}")
    
    def get_movies_by_location(self, location: str) -> List[Movie]:
        """Get movies available at a specific location"""
        if location not in self.locations:
            logger.warning(f"Location not found: {location}")
            return []
        
        return [
            movie for movie in self.movies.values() 
            if movie.location is None or movie.location == location
        ]
    
    def get_special_shows(self, location: str = None) -> List[Movie]:
        """Get special shows (like Women's FDFS)"""
        movies = self.movies.values()
        if location:
            movies = [m for m in movies if m.location is None or m.location == location]
        
        return [movie for movie in movies if movie.special_show]
    
    def get_available_times(self, movie_id: str, location: str) -> List[str]:
        """Get available showtimes for a movie at a location"""
        movie = self.movies.get(movie_id)
        if not movie:
            logger.warning(f"Movie not found: {movie_id}")
            return []
            
        if movie.location and movie.location != location:
            logger.warning(f"Movie {movie_id} not available at {location}")
            return []
            
        return movie.showtimes

# Create global cinema service
cinema_service = CinemaService() 