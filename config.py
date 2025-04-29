import os
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings, Field

# Load environment variables
load_dotenv()

class TwilioSettings(BaseSettings):
    """Twilio configuration settings"""
    account_sid: str = Field(..., env="accountSid")
    auth_token: str = Field(..., env="authToken")
    whatsapp_number: str = Field("whatsapp:+14155238886", env="TWILIO_WHATSAPP_NUMBER")
    
    class Config:
        env_file = '.env'
        case_sensitive = False

class CinemaSettings(BaseSettings):
    """Cinema configuration settings"""
    name: str = Field("Aarthi Grand Cineplex", env="CINEMA_NAME")
    locations: list = Field(["Dindigul"], env="CINEMA_LOCATIONS")
    business_number: str = Field("+917200867909", env="BUSINESS_NUMBER")
    special_show_name: str = Field("Retro", env="SPECIAL_SHOW_NAME")
    cinema_complex: str = Field("Aarthi Grand Cineplex", env="CINEMA_COMPLEX")
    
    class Config:
        env_file = '.env'

class Settings:
    """Main configuration container"""
    def __init__(self):
        try:
            self.twilio = TwilioSettings()
            self.cinema = CinemaSettings()
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
# Create global settings instance
settings = Settings() 