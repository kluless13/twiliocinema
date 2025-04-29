# TwilioCinema WhatsApp Bot

A WhatsApp chatbot built with Twilio to enable automatic conversations with a cinema complex. Users can check movie listings, select showtimes, and book tickets via WhatsApp.

## Features

- Browse current movies and special shows
- Book tickets for regular and special shows (like Women's First Day First Show)
- Select theater location and number of tickets
- Receive booking confirmations

## Project Structure

```
twiliocinema/
├── .env                    # Environment variables (Twilio credentials)
├── app.py                  # Main application entry point
├── config.py               # Configuration loader
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── tests/                  # Test directory
│   ├── __init__.py
│   └── test_*.py           # Test modules
└── modules/                # Core modules
    ├── __init__.py
    ├── bot.py              # Main bot logic
    ├── cinema.py           # Cinema data and operations
    ├── messaging.py        # WhatsApp messaging handler
    ├── session.py          # User session management
    └── utils.py            # Utility functions
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/twiliocinema.git
   cd twiliocinema
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in `.env` file:
   ```
   accountSid='your_twilio_account_sid'
   authToken='your_twilio_auth_token'
   TWILIO_WHATSAPP_NUMBER='whatsapp:+1234567890'
   ```

## Running the Application

Start the Flask server:
```
python app.py
```

The server will be running at `http://localhost:8080`.

## Configuring Twilio Webhook

1. Create a Twilio account at [twilio.com](https://www.twilio.com)
2. Set up a WhatsApp Sandbox in your Twilio console
3. Configure the webhook URL to point to your server's `/webhook` endpoint
   - For local development, you can use [ngrok](https://ngrok.com/) to expose your local server

## Usage Flow

### Women's FDFS Retro Show Booking

1. User sends `#WRETRO` to initiate booking
2. Bot sends terms and conditions
3. User accepts terms by sending `Accept`
4. Bot sends location options
5. User selects location (e.g., `Tirupur`)
6. Bot asks for number of tickets
7. User sends desired number (e.g., `2 Tickets`)
8. Bot confirms booking and informs the cinema admin

## Testing

Run unit tests:
```
python -m pytest
```

## Development 

### Adding New Features

To add a new feature:
1. Create related models in appropriate modules
2. Add handler logic in `MessageHandler` class
3. Update session states if needed
4. Write tests for new functionality

### Movie Data Format

Create or update `data/movies.json` with movie information:

```json
[
  {
    "id": "movie1",
    "title": "Movie Title",
    "description": "Movie description",
    "duration": 120,
    "showtimes": ["10:00 AM", "2:30 PM", "6:00 PM"],
    "price": 150.0,
    "special_show": false,
    "image_url": "https://example.com/movie.jpg"
  }
]
```

## License

This project is licensed under the MIT License.