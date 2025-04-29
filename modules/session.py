"""User session management module"""
from enum import Enum
from typing import Dict, Any, Optional
from loguru import logger
import time

class BookingState(Enum):
    """States for the booking conversation flow"""
    INITIAL = "initial"
    ACCEPTED_TERMS = "accepted_terms"
    TICKETS_SELECTED = "tickets_selected" 
    COMPLETED = "completed"

class UserSession:
    """User session for tracking conversation state"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.state = BookingState.INITIAL
        self.data = {}
        self.last_activity = time.time()
    
    def update_state(self, new_state: BookingState) -> None:
        """Update session state"""
        logger.debug(f"User {self.user_id}: State changed from {self.state} to {new_state}")
        self.state = new_state
        self.last_activity = time.time()
    
    def update_data(self, key: str, value: Any) -> None:
        """Update session data"""
        self.data[key] = value
        self.last_activity = time.time()
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Get session data by key"""
        return self.data.get(key, default)
    
    def reset(self) -> None:
        """Reset session to initial state"""
        logger.info(f"Resetting session for user {self.user_id}")
        self.state = BookingState.INITIAL
        self.data = {}
        self.last_activity = time.time()
    
    @property
    def is_expired(self) -> bool:
        """Check if session is expired (inactive for more than 30 minutes)"""
        return (time.time() - self.last_activity) > (30 * 60)  # 30 minutes

class SessionManager:
    """Manager for user sessions"""
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
    
    def get_session(self, user_id: str) -> UserSession:
        """Get or create user session"""
        if user_id not in self.sessions:
            logger.info(f"Creating new session for user {user_id}")
            self.sessions[user_id] = UserSession(user_id)
        
        # Check for expired session and reset if needed
        session = self.sessions[user_id]
        if session.is_expired:
            logger.info(f"Session expired for user {user_id}, resetting")
            session.reset()
            
        return session
    
    def end_session(self, user_id: str) -> None:
        """End user session"""
        if user_id in self.sessions:
            logger.info(f"Ending session for user {user_id}")
            del self.sessions[user_id]
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions and return count of removed sessions"""
        expired = [user_id for user_id, session in self.sessions.items() if session.is_expired]
        for user_id in expired:
            del self.sessions[user_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        return len(expired)

# Create global session manager
session_manager = SessionManager() 