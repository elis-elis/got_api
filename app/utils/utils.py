import os
import json
from uuid import UUID

from flask import jsonify

# Path to the JSON file where characters are stored
CHARACTERS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'characters.json')


def load_characters():
    """
    Load characters from the JSON file. If the file is empty or missing, return an empty list.
    """
    # Read existing characters from the JSON file
    if os.path.exists(CHARACTERS_JSON_PATH):
        try:
            with open(CHARACTERS_JSON_PATH, 'r') as file:
                characters = json.load(file)
                return characters if isinstance(characters, list) else []
        except (json.JSONDecodeError, ValueError):
            return []  # Handle empty or malformed JSON

    return[]


def save_characters(characters):
    """
    Save the characters list to the JSON file.
    """
    with open(CHARACTERS_JSON_PATH, 'w') as file:
        json.dump(characters, file, indent=4)


def save_and_respond(message, characters, character=None):
    """
    Function to save changes and return a JSON response.
    """
    save_characters(characters)
    response = {"message": message}
    if character:
        response["character"] = character   # Include updated character if applicable
    return jsonify(response), 200


def add_character(new_character):
    """
    Add a new character to the JSON file and return the updated character.
    """
    characters = load_characters()
    new_character["id"] = set_id_for_new_character(characters)
    characters.append(new_character)
    save_characters(characters)
    return new_character


def set_id_for_new_character(characters):
    """
    Determines the next available unique ID for a new character, extracting all existing IDs and find the max ID.
    """
    # Extract all character IDs into a list
    character_ids = []
    for character in characters:
        character_ids.append(character["id"])

    # Find the maximum ID from the list
    if character_ids:  # Check if the list is not empty
        max_id = max(character_ids)
    else:
        max_id = 0  # Default to 0 if there are no characters

    return max_id + 1


def is_valid_uuid(value):
    """
    Check if a value is a valid UUID.
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
