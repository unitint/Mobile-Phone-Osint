import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    DEBUG = True
    
    # API Keys (for future use)
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or None
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or None
    
    # Settings
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    REQUEST_TIMEOUT = 10
    RATE_LIMIT_DELAY = 1  # seconds between requests