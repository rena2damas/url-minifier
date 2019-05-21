from flask import Blueprint

homepage = Blueprint('homepage', __name__)

@homepage.route('/')
def base_route():
    return 'Index Page'