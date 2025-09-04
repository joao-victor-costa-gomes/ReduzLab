import os 
from dotenv import load_dotenv

# This loads the environment variables from the .env file located at the project root.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    RESULTS_FOLDER = os.path.join(basedir, 'results')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH'))