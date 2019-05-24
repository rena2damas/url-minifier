from webapp import create_app, db

if __name__ == "__main__":
    # Create the Flask application
    app = create_app()

    # Create all required tables
    with app.app_context():
        db.create_all()

    # Run the WSGI server application
    app.run()
