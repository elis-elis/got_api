import os
import json
from uuid import UUID


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


def add_character(new_character):
    """
    Add a new character to the JSON file and return the updated character.
    """
    characters = load_characters()
    new_character["id"] = len(characters) + 1  # Assign a new ID
    characters.append(new_character)
    save_characters(characters)
    return new_character


def is_valid_uuid(value):
    """
    Check if a value is a valid UUID.
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
