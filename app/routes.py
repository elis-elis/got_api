"""
Pydantic's validation is just for input data (e.g., when you send data to your API),
but it doesn't directly interact with your database.
That's why I am using this schema to validate incoming data before inserting it into the database.
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Character
from app.schemas import CharacterSchema
from pydantic import ValidationError


# Create a Blueprint
characters_bp = Blueprint("characters", __name__)


@characters_bp.route("/characters", methods=["POST"])
def create_characters():
    try:
        # Validate and parse JSON request body
        data = CharacterSchema(**request.get_json())

        # Create new Character instance
        character = Character(**data.dict())

        db.session.add(character)
        db.session.commit()

        return jsonify({"message": "Character created successfully!"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
