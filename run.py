from webapp import app, db

if __name__ == "__main__":
    # Create all required tables
    db.create_all()

    # Run the WSGI application
    app.run()
