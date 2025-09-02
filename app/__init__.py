from flask import Flask
from config import Config

def create_app(config_class=Config):

    # Creates the main application instance.
    app = Flask(__name__)

    # Loads the configuration from the object we passed (config.Config).
    app.config.from_object(config_class)

    # Here is where we will register our Blueprints.
    # Blueprints are like mini-applications that help organize routes.
    from .main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    # Returns the created and configured application instance.
    return app