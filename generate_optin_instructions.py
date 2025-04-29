#!/usr/bin/env python
"""
Generate opt-in instructions for WhatsApp recipients
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

def get_twilio_sandbox_info():
    """Get WhatsApp Sandbox information from Twilio"""
    try:
        # Initialize Twilio client
        client = Client(settings.twilio.account_sid, settings.twilio.auth_token)
        
        # Get sandbox information
        whatsapp_sender = settings.twilio.whatsapp_number
        if whatsapp_sender.startswith('whatsapp:'):
            whatsapp_sender = whatsapp_sender[9:]  # Remove the 'whatsapp:' prefix
            
        print("\n=== WhatsApp Sandbox Opt-In Instructions ===\n")
        print(f"1. Save this number in your contacts: {whatsapp_sender}")
        print(f"2. Send the following message to {whatsapp_sender} on WhatsApp:")
        print(f"\n   join <sandbox-code>\n")
        print("   Note: Replace <sandbox-code> with the code from your Twilio WhatsApp Sandbox settings")
        print("   You can find this code in your Twilio Console under Messaging > Try it out > WhatsApp")
        print("\n3. Wait for a confirmation message from Twilio")
        print("4. Once confirmed, the recipient can receive messages from your bot\n")
            
    except Exception as e:
        print(f"Error retrieving sandbox information: {str(e)}")
        print("\nYou can find your WhatsApp Sandbox join code in the Twilio Console:")
        print("1. Log in to your Twilio account: https://www.twilio.com/console")
        print("2. Navigate to Messaging > Try it out > WhatsApp")
        print("3. Find your sandbox code and share it with recipients\n")

if __name__ == "__main__":
    get_twilio_sandbox_info() 