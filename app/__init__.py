"""
This file is responsible for:
- Creating and configuring a Flask application instance.
- Setting up the SQLAlchemy database connection.
- Enabling database migrations using Flask-Migrate.
- Configuring JWT authentication for secure API access.

Usage:
    - The `create_app()` function is called to initialize the Flask app.
    - The app is configured using the settings in `app.config.Config`.
    - Extensions like `db` (SQLAlchemy), `migrate` (Flask-Migrate), and `jwt` (JWTManager) are initialized.
    - Blueprints can be registered within the `create_app()` function to modularize routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config


# Initialize database / extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    """
    This function creates a new Flask application instance, applies configuration settings,
    initializes extensions (database, migration, JWT authentication), and registers blueprints.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.routes import characters_bp, auth_protected_bp
    from app.auth import auth_bp

    app.register_blueprint(characters_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(auth_protected_bp, url_prefix="/protected")

    return app
