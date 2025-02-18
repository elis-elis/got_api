from flask import jsonify
import logging


# Set up logging
logger = logging.getLogger(__name__)


def handle_404(error):
    return jsonify({"message": "This resource was not found. Please check the URL. And maybe a smile."}), 404


def handle_500(error):
    return jsonify({"message": "Oops! Internal server error. Please try again later, if you can."}), 500


def handle_sqlalchemy_error(error):
    """
    Handles SQLAlchemy-related database errors safely.
    Logs the detailed error but returns a generic message to the user.
    """
    logger.error(f"Database error occurred: {str(error)}")  # Log for debugging (internal use)

    return jsonify({"message": f"Ouch! Something went wrong with the database. Please try again later."}), 500


def handle_validation_error(error):
    return jsonify({"message": "Ah! Validation error", "errors": error.errors()}), 400
