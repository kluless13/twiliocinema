#!/usr/bin/env python
"""
Send WhatsApp invitation with opt-in instructions
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

def send_whatsapp_invitation(to_number, sandbox_code="most-bean"):
    """Send WhatsApp invitation to join the bot service"""
    try:
        # Initialize Twilio client
        client = Client(settings.twilio.account_sid, settings.twilio.auth_token)
        
        # Ensure the recipient is already a valid WhatsApp recipient
        # This only works if they've already joined your sandbox
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        # Get sandbox information
        whatsapp_sender = settings.twilio.whatsapp_number
        
        # Craft the invitation message
        message_body = (
            "Welcome to Sri Sakthi Cinemas WhatsApp Bot! 🎬\n\n"
            "To book tickets for our Women's FDFS-RETRO show, just send #WRETRO"
        )
        
        # Check if recipient is already registered, if yes, send direct welcome
        # If not, the message will fail, and we need to ask them to join the sandbox
        try:
            message = client.messages.create(
                body=message_body,
                from_=whatsapp_sender,
                to=to_number
            )
            print(f"✅ Welcome message sent via WhatsApp to {to_number}")
            print(f"Message SID: {message.sid}")
            return True
        except Exception as e:
            if "is not currently subscribed" in str(e):
                print(f"❌ The recipient {to_number} is not subscribed to your sandbox.")
                print(f"\nPlease share these instructions with them:\n")
                with open('sandbox_instructions.txt', 'r') as f:
                    print(f.read())
            else:
                raise e
                
    except Exception as e:
        print(f"❌ Failed to send invitation: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_whatsapp_invitation.py <phone_number> [sandbox_code]")
        print("Example: python send_whatsapp_invitation.py +919894775962 most-bean")
        sys.exit(1)
    
    # Get phone number from command line
    to_number = sys.argv[1]
    
    # Get optional sandbox code
    sandbox_code = sys.argv[2] if len(sys.argv) > 2 else "most-bean"
    
    # Send invitation
    send_whatsapp_invitation(to_number, sandbox_code) 