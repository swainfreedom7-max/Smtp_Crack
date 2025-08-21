import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SESSION_LIFETIME = 1800
    MAX_ENTRIES = 5000
    TIMEOUT = 10