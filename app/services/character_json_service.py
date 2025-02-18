from app.utils.json_utils import save_characters
from app.utils.filters import apply_filters
from app.utils.sorting import apply_sorting
from app.utils.json_utils import load_characters


def show_characters_json(filters, sort_by, sort_order, limit, skip):
    """
    Fetch characters from the JSON file with filtering, sorting, and pagination.
    Returns both count (paginated result) & total (unpaginated count).
    """
    try:
        characters = load_characters()

        # Apply filters dynamically
        filtered_characters = apply_filters(characters, filters)

        # Get total count before pagination
        total_count = len(filtered_characters)

        # Apply sorting
        sorted_characters = apply_sorting(filtered_characters, sort_by, sort_order)

        # Apply pagination
        paginated_characters = sorted_characters[skip: skip + limit]   # This is Python's list slicing
        # skip → The starting index (how many items to skip)
        # skip + limit → The ending index (where to stop, exclusive)
        # This technique prevents loading too much data at once by returning only a small portion of the full list

        # Return the result (paginated data + metadata)
        return {
            "characters": paginated_characters,
            "count": len(paginated_characters),  # Number of characters returned after pagination
            "total": total_count  # Total characters before pagination
        }

    except Exception as e:
        return {"error": str(e)}


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
