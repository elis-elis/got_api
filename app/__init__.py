"""
This file:
Creates a Flask app.
Configures the database.
Initialize extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

# Initialize database
db = SQLAlchemy()
jwt = JWTManager


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
