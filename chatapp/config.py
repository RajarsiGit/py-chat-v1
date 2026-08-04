import os


class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    CHAT_PIN = os.environ.get('CHAT_PIN', '2468')
