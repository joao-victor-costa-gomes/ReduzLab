from flask import Flask
from app.config import Config

def create_app():
    # Create a Flask application and apply the configurations from config.py
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register the routes blueprint with the application 
    from app.routes import main
    app.register_blueprint(main)

    return app
