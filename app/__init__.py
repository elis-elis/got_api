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
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.config import Config
from app.error_handlers import handle_404, handle_500, handle_sqlalchemy_error, handle_validation_error


# Initialize database / extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    """
    This function creates a new Flask application instance, applies configuration settings,
    initializes extensions (database, migration, JWT authentication), registers blueprints and error handlers.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.routes import characters_bp
    from app.auth import auth_bp

    app.register_blueprint(characters_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Register Error Handlers
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(SQLAlchemyError, handle_sqlalchemy_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    return app
