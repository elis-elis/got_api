from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app import handle_500, handle_validation_error
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.character_schema import CharacterJSONSchema
from app.utils.json_utils import load_characters, save_and_respond
from app.services.character_json_service import add_character


# Create a Blueprint for character-related routes
characters_json_bp = Blueprint("characters", __name__)


@characters_json_bp.route('/character/json', methods=['POST'])
@jwt_required()  # This will ensure only authorized users can create characters
def create_character():
    """
    Endpoint to create a new character and store it in 'characters.json'.
    Check if data is valid (Pydantic schema validation).
    Load existing characters from the 'characters.json' file.
    Add the new character to the in-memory list.
    Save the updated list back to the 'characters.json' file.
    Return success response.
    Consideration: The data is lost if the server is restarted. For more permanent storage, switch to a database.
    """
    try:
        # Get the user identity from the JWT
        current_user = get_jwt_identity()  # for authentication purpose, although not used here directly

        # Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Create a new character
        # Use Pydantic to validate the incoming character data
        validated_data = CharacterJSONSchema(**data).dict()
        new_character = add_character(validated_data)

        return jsonify({"message": "Character created successfully", "character": new_character}), 201

    except ValidationError as ve:
        return handle_validation_error(ve)

    except Exception as e:
        return handle_500(e)


@characters_json_bp.route('/characters/json/<int:character_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def handle_character_json(character_id):
    """
    Handles fetching (GET), updating (PATCH), and deleting (DELETE) a character by ID in the JSON file.
    """
    characters = load_characters()

    # character = next((char for char in characters if char["id"] == character_id), None)
    character = None
    for char in characters:
        if char["id"] == character_id:
            character = char
            break

    if not character:
        return jsonify({"message": "Character not found"}), 404

    try:
        if request.method == 'GET':
            return jsonify(character), 200

        if request.method == 'PATCH':
            data = request.get_json()
            if not data:
                return jsonify({"message": "No data provided"}), 400

            # Validate and update character fields dynamically using Pydantic schema
            validated_data = CharacterJSONSchema(**{**character, **data}).dict(exclude_unset=True)

            # Update the character in the list
            for key, value in validated_data.items():
                character[key] = value

            return save_and_respond("Voilà! Character updated successfully", characters, character)

        elif request.method == 'DELETE':
            # Creates a new list excluding the character with character_id
            characters = [char for char in characters if char["id"] != character_id]

            return save_and_respond("Character deleted successfully from JSON.", characters)

    except ValidationError as ve:
        return handle_validation_error(ve)

    except Exception as e:
        return handle_500(e)
