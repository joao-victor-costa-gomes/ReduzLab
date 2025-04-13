import os
from dotenv import load_dotenv

# Load important variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path) 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    RESULTS_FOLDER = os.path.abspath(os.environ.get('RESULTS_FOLDER', 'results'))
    SAMPLES_FOLDER = os.environ.get('SAMPLES_FOLDER', os.path.join(os.getcwd(), 'samples'))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024)) # 100MB