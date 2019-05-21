from flask import Flask
from webapp.controllers.homepage import homepage
import os

# Define the WSGI application object
app = Flask(__name__)

# Different environments
config = {
    'production': 'webapp.configs.config.ProductionConfig',
    'development': 'webapp.configs.config.DevelopmentConfig',
    'testing': 'webapp.configs.config.TestingConfig',
    'default': 'webapp.configs.config.DevelopmentConfig'
}

# Configurations
env = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[env])  # object-based default configuration

# Register blueprints
app.register_blueprint(homepage)