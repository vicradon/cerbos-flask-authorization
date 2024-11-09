import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'somerandomsecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False