from flask import Flask, session, request, current_app
from config import Config
from flask_babel import Babel

babel = Babel

def create_app(config_class=Config):

    # Creates the main application instance.
    app = Flask(__name__)

    babel.init_app(app)

    # Loads the configuration from the object we passed (config.Config).
    app.config.from_object(config_class)

    # Here is where we will register our Blueprints.
    # Blueprints are like mini-applications that help organize routes.
    from .main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    # Returns the created and configured application instance.
    return app

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])