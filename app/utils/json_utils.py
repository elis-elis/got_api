import os
import json
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
