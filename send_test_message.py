#!/usr/bin/env python
"""
Test script to send a WhatsApp message using Twilio
"""
import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client
from loguru import logger

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.utils import setup_logging
from config import settings

# Setup logging
setup_logging()

def send_test_message(to_number: str, message: str = "Welcome to Sri Sakthi Cinemas! 🎬"):
    """Send a test WhatsApp message using Twilio"""
    try:
        # Ensure number has correct format for WhatsApp
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
            
        # Initialize Twilio client
        client = Client(settings.twilio.account_sid, settings.twilio.auth_token)
        
        # Log attempt
        logger.info(f"Sending test message to {to_number}")
        
        # Send message
        message = client.messages.create(
            from_=settings.twilio.whatsapp_number,
            body=message,
            to=to_number
        )
        
        logger.info(f"Message sent successfully. SID: {message.sid}")
        return True, message.sid
        
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    # Get the number from command line argument or use default
    to_number = sys.argv[1] if len(sys.argv) > 1 else "+919047027504"
    
    # Test message content
    test_message = "Hello! This is a test message from Sri Sakthi Cinemas WhatsApp Bot. Reply with #WRETRO to book tickets for Women's FDFS-RETRO show."
    
    # Send the message
    success, result = send_test_message(to_number, test_message)
    
    if success:
        print(f"✅ Message sent successfully. SID: {result}")
    else:
        print(f"❌ Failed to send message: {result}") 