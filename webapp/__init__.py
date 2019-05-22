from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# The WSGI application object
app = Flask(__name__)

# Different environments
config = {
    'production': 'webapp.configs.config.ProductionConfig',
    'development': 'webapp.configs.config.DevelopmentConfig',
    'testing': 'webapp.configs.config.TestingConfig',
    'default': 'webapp.configs.config.DevelopmentConfig'
}

# Loading configurations
env = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[env])  # object-based default configuration

# Linking application to database
db = SQLAlchemy(app)

# Importing and registering blueprints
from webapp.controllers.minifier import minifier
app.register_blueprint(minifier)
