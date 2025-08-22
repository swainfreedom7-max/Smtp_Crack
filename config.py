import os

class Config:
    SECRET_KEY = os.urandom(24).hex()  # Auto-generates secure random key
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SESSION_LIFETIME = 1800
    MAX_ENTRIES = 5000
    TIMEOUT = 10
    PORT = int(os.environ.get('PORT', 10000))