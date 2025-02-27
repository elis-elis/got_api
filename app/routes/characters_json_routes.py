from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app import handle_500, handle_validation_error
from flask_jwt_extended import jwt_required
from app.schemas.character_schema import CharacterJSONSchema
from app.utils.json_utils import load_characters, save_and_respond
from app.services.character_json_service import add_character, show_characters_json
from app.utils.pagination import get_pagination_params

# Create a Blueprint for character-related routes
characters_json_bp = Blueprint("characters", __name__)


@characters_json_bp.route('/characters/json', methods=['GET'])
def list_characters_json():
    """
    Fetch characters from JSON with optional filtering, sorting, and pagination.
    Convert query parameters to a dictionary (filters).
    Extract sorting fields (sort_by, sort_order).
    Extract pagination fields (limit, skip).
    Remaining filters are used for filtering characters dynamically.

    Example Request:
    GET /characters/json?house=Lannister&sort_by=name&limit=5
    """
    # Get query parameters for filtering, sorting, and pagination
    filters = request.args.to_dict()
    sort_by = filters.pop("sort_by", None)
    sort_order = filters.pop("sort_order", "asc")

    # Extract pagination parameters (returns "random" if both are missing)
    limit, skip = get_pagination_params()

    result = show_characters_json(filters, sort_by, sort_order, limit, skip)

    # Check if the result contains an error (by checking if it is a dictionary and contains the 'error' key)
    if isinstance(result, dict) and "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result), 200


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
