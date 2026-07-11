import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # API Keys
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    
    # Settings
    USER_AGENT = os.environ.get('USER_AGENT') or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 10))
    RATE_LIMIT_DELAY = int(os.environ.get('RATE_LIMIT_DELAY', 1))
    
    # Flask settings
    SESSION_COOKIE_SECURE = not DEBUG
    REMEMBER_COOKIE_SECURE = not DEBUG