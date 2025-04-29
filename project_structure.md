# Project Structure

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