from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError


def handle_404(error):
    return jsonify({"message": "This resource was not found. Please check the URL."}), 404


def handle_500(error):
    return jsonify({"message": "Internal server error. Please try again later."}), 500


def handle_sqlalchemy_error(error):
    return jsonify({"message": f"Database error: {str(error)}"}), 500


def handle_validation_error(error):
    return jsonify({"message": "Validation error", "errors": error.errors()}), 400
