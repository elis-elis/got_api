from flask import request


def get_pagination_params():
    """
    Extract and validate pagination parameters.
    If no limit/skip is defined, return a random subset of 20 characters.

    Query Parameters:
    - limit: Number of characters to return (default: 20)
    - skip: Number of characters to skip (default: 0)
    """
    limit = request.args.get('limit', type=int, default=20)
    skip = request.args.get('skip', type=int, default=0)

    # If no limit/skip is provided, we return a random 20 characters
    if limit is None and skip is None:
        return "random", 20  # Special flag to indicate random selection

    # Default values
    limit = limit if not None else 20
    skip = skip if not None else 0

    if limit <= 0:
        raise ValueError("Limit must be greater than 0.")
    if skip < 0:
        raise ValueError("Skip cannot be negative.")

    return limit, skip
