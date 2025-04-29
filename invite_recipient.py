#!/usr/bin/env python
"""
Send an invitation to join the Twilio WhatsApp Sandbox
"""
import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client
from loguru import logger

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from config import settings

def send_join_instructions(to_number, sandbox_code=None):
    """Send instructions to join the WhatsApp sandbox"""
    try:
        # Initialize Twilio client
        client = Client(settings.twilio.account_sid, settings.twilio.auth_token)
        
        # Format the phone number for SMS (not WhatsApp, since they can't receive WhatsApp yet)
        if to_number.startswith('whatsapp:'):
            to_number = to_number[9:]  # Remove 'whatsapp:' prefix
        
        # Get sandbox information
        whatsapp_sender = settings.twilio.whatsapp_number
        if whatsapp_sender.startswith('whatsapp:'):
            whatsapp_sender = whatsapp_sender[9:]  # Remove 'whatsapp:' prefix
        
        # Craft the invitation message
        if not sandbox_code:
            message_body = (
                f"To chat with Sri Sakthi Cinemas on WhatsApp, please:\n\n"
                f"1. Save this number in your contacts: {whatsapp_sender}\n\n"
                f"2. Open WhatsApp and send the message 'join <sandbox-code>' to this number.\n\n"
                f"Replace <sandbox-code> with the code from your Twilio WhatsApp Sandbox settings."
            )
        else:
            message_body = (
                f"To chat with Sri Sakthi Cinemas on WhatsApp, please:\n\n"
                f"1. Save this number in your contacts: {whatsapp_sender}\n\n"
                f"2. Open WhatsApp and send the message 'join {sandbox_code}' to this number."
            )
        
        # Send the SMS invitation
        message = client.messages.create(
            body=message_body,
            from_=settings.twilio.whatsapp_number.replace('whatsapp:', ''),  # Use SMS from number
            to=to_number
        )
        
        print(f"✅ Invitation sent via SMS to {to_number}")
        print(f"Message SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send invitation: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python invite_recipient.py <phone_number> [sandbox_code]")
        print("Example: python invite_recipient.py +919894775962 gentle-moon")
        sys.exit(1)
    
    # Get phone number from command line
    to_number = sys.argv[1]
    
    # Get optional sandbox code
    sandbox_code = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Send invitation
    send_join_instructions(to_number, sandbox_code) 