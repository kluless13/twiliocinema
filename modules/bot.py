"""Main WhatsApp Cinema Bot logic"""
from loguru import logger
from modules.messaging import message_handler
from modules.session import session_manager

class CinemaBot:
    """Main bot class that orchestrates the WhatsApp cinema booking system"""
    def __init__(self):
        self.message_handler = message_handler
        logger.info("Cinema Bot initialized and ready")
    
    def process_incoming_message(self, sender: str, message_body: str) -> None:
        """Process incoming WhatsApp message"""
        logger.debug(f"Received message from {sender}: {message_body}")
        
        try:
            # Handle the message based on session state
            self.message_handler.handle_message(sender, message_body)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Send error message to user
            self.message_handler.messaging.send_message(
                sender,
                "Sorry, there was an error processing your request. Please try again."
            )
    
    def cleanup(self) -> None:
        """Perform periodic cleanup tasks"""
        # Clean up expired sessions
        expired_count = session_manager.cleanup_expired_sessions()
        logger.info(f"Cleaned up {expired_count} expired sessions")

# Create global bot instance
cinema_bot = CinemaBot() 