from dotenv import load_dotenv
import os

# Load environment variables from .env or sql.env 
# (assuming you named your file sql.env)
load_dotenv('sql.env')

class Config:
    # App Configuration
    APP_PORT = os.getenv('PORT', 5000)
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-please-change-it')

    # JWT Configuration (Uses the same SECRET_KEY)
    JWT_SECRET_KEY = SECRET_KEY
    
    # Database Configuration
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    # Construct the SQLAlchemy Database URI using the environment variables
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False # Set to True to see SQL queries in console

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

def get_config():
    # You would typically switch this based on an environment variable, 
    # but we default to Development for now.
    return DevelopmentConfig()