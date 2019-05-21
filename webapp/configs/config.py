class Config:

    # Statement for enabling the development environment
    DEBUG = False
    TESTING = False

    # Define the database - we are working with
    # SQLite for this example
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = False

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    # Key for form
    WTF_CSRF_SECRET_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "dw65vrcgQO"


class ProductionConfig(Config):
    ENV = 'production'
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    LOG_LEVEL = 'INFO'


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    LOG_LEVEL = 'DEBUG'
