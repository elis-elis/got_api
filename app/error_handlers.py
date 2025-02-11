from flask import jsonify


def handle_404(error):
    return jsonify({"message": "This resource was not found. Please check the URL. And maybe a smile."}), 404


def handle_500(error):
    return jsonify({"message": "Oops! Internal server error. Please try again later, if you can."}), 500


def handle_sqlalchemy_error(error):
    return jsonify({"message": f"Ouch! Database error: {str(error)}"}), 500


def handle_validation_error(error):
    return jsonify({"message": "Ah! Validation error", "errors": error.errors()}), 400
