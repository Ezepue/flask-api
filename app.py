from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize the database with the app
    db.init_app(app)

    # Import and register routes (avoids circular import)
    import routes

    app.register_blueprint(routes.bp)

    return app
