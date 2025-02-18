import logging
from flask import jsonify


# Set up logging
logger = logging.getLogger(__name__)


def handle_404(error):
    """
    Handles 404 Not Found errors.
    """
    return jsonify({
        "message": "This resource was not found. Please check the URL. And maybe a smile."
    }), 404


def handle_500(error):
    """
    Handles generic internal server errors (500).
    """
    return jsonify({
        "message": "Oops! Internal server error. Please try again later, if you can."
    }), 500


def handle_sqlalchemy_error(error):
    """
    Handles database-related errors (SQLAlchemy exceptions).
    Logs the detailed error but returns a generic message to the user.
    """
    logger.error(f"Database error occurred: {str(error)}")  # Log for debugging (internal use)

    return jsonify({
        "message": f"Ouch! Something went wrong with the database. Please try again later."
    }), 500


def handle_validation_error(error):
    """
    Handles validation errors when input data does not meet schema requirements.
    Logs the validation error details and returns a message with specific errors.
    """
    logger.warning(f"Validation error: {error.errors()}")  # Log validation issues (warning level)

    return jsonify({
        "message": "Ah! Validation error",
        "errors": error.errors()
    }), 400
