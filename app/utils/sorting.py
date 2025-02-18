from flask import request
from sqlalchemy import asc, desc
from app.models.character_model import Character, House, Strength


ALLOWED_SORT_FIELDS = {"name", "age", "house", "role", "nickname", "animal", "symbol", "death", "strength"}


def get_sorting_params():
    """Extract and validate sorting parameters from the request arguments."""

    sort_by = request.args.get('sort_by', type=str, default="name")
    sort_order = request.args.get('sort_order', type=str, default="asc").lower()

    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "name"  # Default if invalid field is given

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    return sort_by, sort_order


def apply_sorting(query, sort_by, sort_order):
    """
    Modify an existing query object by dynamically adding sorting and joins based on the sort_by and sort_order
    parameters. The query object is created earlier in the code, and passed into this function as an argument.
    The Character model has a relationship with the House and Strength models. When sorting by either of these fields,
    need to perform a SQL join between the Character table and the related table (House or Strength)
    in order to access the field it is sorted by.
    """
    if sort_by not in ALLOWED_SORT_FIELDS:
        # sort_by - the column name passed by the user
        return query  # If the sorting field is not recognized, return the query unchanged

    # Map of sort fields to their corresponding columns (and optional joins)
    sort_fields = {
        "name": Character.name,
        "age": Character.age,
        "house": House.name,
        "role": Character.role,
        "nickname": Character.nickname,
        "animal": Character.animal,
        "symbol": Character.symbol,
        "death": Character.death,
        "strength": Strength.description
    }
    # Check if the field exists in the map
    if sort_by not in sort_fields:
        return query  # If field is not found, return query unchanged

    # Determine the sorting function
    sort_func = asc if sort_order == "asc" else desc

    # If sorting by 'house' or 'strength', perform the join first
    if sort_by in ["house", "strength"]:
        # conditional expression
        query = query.join(House if sort_by == "house" else Strength)

    # Apply the sorting
    return query.order_by(sort_func(sort_fields[sort_by]))
    # query = query.order_by(sort_func(Strength.description))  # Sorting by strength description
    # query = query.order_by(sort_func(House.name))  # Sorting by house name
