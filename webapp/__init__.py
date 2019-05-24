from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Different environments
config = {
    'production': 'webapp.configs.config.ProductionConfig',
    'development': 'webapp.configs.config.DevelopmentConfig',
    'testing': 'webapp.configs.config.TestingConfig',
    'default': 'webapp.configs.config.DevelopmentConfig'
}

# Application root path
root_path = os.path.dirname(__file__)

# SQLite database
db = SQLAlchemy()

def create_app(env='default'):
    """Create a new app"""

    # The WSGI application object
    app = Flask("URL Minifier")

    # Loading configurations
    env = os.getenv('FLASK_CONFIGURATION', env)
    app.config.from_object(config[env])  # object-based default configuration

    # Linking application to database
    db.init_app(app)

    # Importing and registering blueprints
    from webapp.controllers.minifier import minifier
    app.register_blueprint(minifier)

    @app.after_request
    def add_header(response):
        """Setting every response content type to json"""
        response.headers['Content-Type'] = 'application/json'
        return response

    return app
