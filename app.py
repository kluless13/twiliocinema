"""
WhatsApp Cinema Booking Bot
--------------------------
A WhatsApp chatbot using Twilio to enable automatic movie ticket bookings
for a cinema complex.
"""
import os
import sys
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from loguru import logger

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.utils import setup_logging
from modules.bot import cinema_bot
from modules.session import session_manager
from config import settings

# Initialize Flask app
app = Flask(__name__)

# Setup logging
setup_logging()
logger.info("Starting WhatsApp Cinema Bot")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp webhook"""
    try:
        # Get incoming message details
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        logger.info(f"Received webhook from {sender}")
        
        # Process the message
        cinema_bot.process_incoming_message(sender, incoming_msg)
        
        # Return empty TwiML response
        resp = MessagingResponse()
        return str(resp)
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return Response(status=500)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'ok'}

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    return f'WhatsApp Cinema Bot for {settings.cinema.name} is running'

def create_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Create sample movie data if it doesn't exist
    if not os.path.exists('data/movies.json'):
        import json
        sample_data = [
            {
                "id": "wretro1",
                "title": "Women's FDFS-RETRO",
                "description": "Special show for women only",
                "duration": 180,
                "showtimes": ["9:00 AM"],
                "price": 150.0,
                "special_show": True,
                "image_url": None
            }
        ]
        with open('data/movies.json', 'w') as f:
            json.dump(sample_data, f, indent=2)
        logger.info("Created sample movie data")

if __name__ == '__main__':
    create_data_directory()
    logger.info(f"Starting server with Twilio account {settings.twilio.account_sid}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False) 