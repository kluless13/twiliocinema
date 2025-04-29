"""WhatsApp messaging handler module"""
from typing import Dict, List, Any, Optional
from loguru import logger
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config import settings
from modules.session import BookingState, session_manager

class WhatsAppMessaging:
    """WhatsApp messaging handler using Twilio"""
    def __init__(self):
        """Initialize with Twilio client"""
        try:
            self.client = Client(settings.twilio.account_sid, settings.twilio.auth_token)
            self.whatsapp_number = settings.twilio.whatsapp_number
            logger.info("WhatsApp messaging client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize WhatsApp messaging: {str(e)}")
            raise
    
    def send_message(self, to: str, body: str, media_url: Optional[List[str]] = None) -> bool:
        """Send WhatsApp message with optional media"""
        try:
            if not to.startswith('whatsapp:'):
                to = f'whatsapp:{to}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=body,
                to=to,
                media_url=media_url
            )
            logger.info(f"Message sent to {to}: {message.sid}")
            return True
        except TwilioRestException as e:
            logger.error(f"Twilio error sending message to {to}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error sending message to {to}: {str(e)}")
            return False
    
    def send_welcome_message(self, to: str) -> bool:
        """Send welcome message with options"""
        welcome_text = (
            f"Welcome to {settings.cinema.name}! 🎬\n\n"
            "How can I help you today?\n\n"
            "1. View Current Movies\n"
            "2. Check Special Shows\n"
            "3. Book Tickets\n"
            "4. Location & Hours"
        )
        return self.send_message(to, welcome_text)
    
    def send_terms_and_conditions(self, to: str, show_type: str) -> bool:
        """Send terms and conditions for special shows"""
        if show_type == "WRETRO":
            terms_text = (
                "Women's FDFS (9:00 AM Show) — Retro Movie\n\n"
                "Terms and Conditions\n\n"
                "1. Entry is strictly restricted to women. This is an exclusive Women's First Day First Show (FDFS).\n"
                "2. ⁠Children up to 10 years of age may accompany women.\n\n"
                "Please reply 'Accept' to confirm or 'Decline' to cancel."
            )
            return self.send_message(to, terms_text)
        return False
    
    def send_ticket_options(self, to: str) -> bool:
        """Send ticket quantity selection options"""
        ticket_text = (
            "Women's FDFS (9:00 AM Show) — Retro Movie\n"
            "📍 Location: Aarthi Grand Cineplex, Dindigul\n\n"
            "How many tickets would you like to book? Please reply with a number."
        )
        return self.send_message(to, ticket_text)
    
    def send_confirmation(self, to: str, tickets: int) -> bool:
        """Send booking confirmation message"""
        confirmation_text = (
            "Thank you! We'll be sharing the ticket link with you shortly.\n"
            "Please book your tickets and enjoy the Women's Special FDFS at Aarthi Grand Cineplex, Dindigul. 😁"
        )
        return self.send_message(to, confirmation_text)

class MessageHandler:
    """Handler for incoming WhatsApp messages"""
    def __init__(self):
        self.messaging = WhatsAppMessaging()
    
    def handle_message(self, from_number: str, body: str) -> None:
        """Process incoming message based on user session state"""
        user_id = from_number
        session = session_manager.get_session(user_id)
        
        # Clean up the incoming message
        clean_body = body.strip().lower()
        
        # Process message based on current state
        if session.state == BookingState.INITIAL:
            if "#wretro" in clean_body:
                self.messaging.send_terms_and_conditions(from_number, "WRETRO")
                session.update_state(BookingState.ACCEPTED_TERMS)
                session.update_data("show_type", "WRETRO")
            else:
                self.messaging.send_welcome_message(from_number)
                
        elif session.state == BookingState.ACCEPTED_TERMS:
            if "accept" in clean_body:
                # Since we have only one location, we'll use that and skip to tickets
                location = settings.cinema.locations[0]
                session.update_data("location", location)
                self.messaging.send_ticket_options(from_number)
                session.update_state(BookingState.TICKETS_SELECTED)
            elif "decline" in clean_body:
                self.messaging.send_welcome_message(from_number)
                session.reset()
            else:
                # Invalid response, re-prompt
                self.messaging.send_message(
                    from_number, 
                    "Please respond with 'Accept' or 'Decline' to continue."
                )
                
        elif session.state == BookingState.TICKETS_SELECTED:
            try:
                # Try to extract the number of tickets
                # This will handle inputs like "2", "2 tickets", etc.
                tickets_text = clean_body
                digits = ''.join(filter(str.isdigit, tickets_text))
                
                if digits:
                    tickets = int(digits)
                    if tickets > 0:
                        session.update_data("tickets", tickets)
                        self.messaging.send_confirmation(from_number, tickets)
                        session.update_state(BookingState.COMPLETED)
                        
                        # In a real system, notify admin about new booking
                        logger.info(f"New booking: {user_id}, {tickets} tickets at {session.get_data('location')}")
                        return
                
                # If we reach here, there was an issue with the ticket number
                self.messaging.send_message(
                    from_number,
                    "Please enter a valid number of tickets (e.g., '2' or '3 tickets')."
                )
            except Exception as e:
                logger.error(f"Error processing ticket number: {str(e)}")
                self.messaging.send_message(
                    from_number,
                    "Please enter a valid number of tickets (e.g., '2' or '3 tickets')."
                )
        
        else:
            # Default fallback for any other state
            self.messaging.send_welcome_message(from_number)
            session.reset()

# Create global message handler
message_handler = MessageHandler() 