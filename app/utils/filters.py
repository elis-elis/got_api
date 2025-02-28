from flask import request
from app.models.character_model import Character, House, Strength


# Define constraints
MAX_STRING_LENGTH = 50  # Prevents excessively long filter values
AGE_MIN, AGE_MAX = 0, 150  # Reasonable age range for validation


def get_filter_params():
    """
    Collects filter parameters from the URL query string, ensuring proper type validation.
    Returns a dictionary of valid filters, ignoring invalid inputs.
    """
    filters = {}

    # Define allowed string fields with max length enforcement
    string_fields = ["name", "house", "strength", "animal", "role"]
    for field in string_fields:
        value = request.args.get(field, type=str)
        if value:
            if len(value) > MAX_STRING_LENGTH:
                raise ValueError(f"Invalid value for {field}. Max length is {MAX_STRING_LENGTH} characters.")
            filters[field] = value.strip()  # Strip leading/trailing spaces

    # Validate integer filters
    int_fields = {
        "age": (AGE_MIN, AGE_MAX),
        "age_more_than": (AGE_MIN, AGE_MAX),
        "age_less_than": (AGE_MIN, AGE_MAX),
        "strength_id": (1, None),  # IDs must be positive numbers
        "house_id": (1, None)  # IDs must be positive numbers
    }

    for field, (min_val, max_val) in int_fields.items():
        value = request.args.get(field)
        if value is not None:
            if not value.isdigit():  # faster check, .isdigit() ensures only numbers are accepted before conversion
                raise ValueError(f"Uff. Invalid value for {field}. Must be a number.")

            num_value = int(value)

            # Enforce valid range (if max_val is specified)
            if num_value < min_val or (max_val and num_value > max_val):
                raise ValueError(f"Invalid value for {field}. Must be between {min_val} and {max_val}.")

            filters[field] = num_value

    return filters


def apply_filters(query, filters):
    """
    The function takes in a SQLAlchemy query 'query' and a dictionary of filters 'filters',
    and it applies those filters to the query before executing it.
    It checks if specific filters exist in the 'filters' dictionary.
    If the filter is present, it applies a corresponding filter condition to the query.
    After all filters have been applied, it returns the modified query.
    """
    if "name" in filters:
        # ilike(): case-insensitive matching, f"%{filters['name']}%": allows for partial matches
        query = query.filter(Character.name.ilike(f"%{filters['name']}%"))

    # Filtering by house name using a join to the houses table
    if "house" in filters:
        query = query.join(House).filter(House.name.ilike(f"%{filters['house']}%"))

    # Filtering by strength description using a join to the strengths table
    if "strength" in filters:
        query = query.join(Strength).filter(Strength.description.ilike(f"%{filters['strength']}%"))

    if "role" in filters:
        query = query.filter(Character.role.ilike(f"%{filters['role']}%"))

    if "animal" in filters:
        query = query.filter(Character.animal.ilike(f"%{filters['animal']}%"))

    if "age" in filters:
        query = query.filter(Character.age == filters["age"])

    if "age_more_than" in filters:
        query = query.filter(Character.age >= filters["age_more_than"])

    if "age_less_than" in filters:
        query = query.filter(Character.age <= filters["age_less_than"])

    # Filtering by house ID (exact match) using a join with the House table
    if "house_id" in filters:
        query = query.filter(Character.house_id == filters["house_id"])

    # Filtering by strength ID (exact match) using a join with the Strength table
    if "strength_id" in filters:
        query = query.filter(Character.strength_id == filters["strength_id"])

    return query
