from app.utils.json_utils import load_characters, save_characters


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
