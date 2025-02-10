from uuid import UUID


def is_valid_uuid(value):
    """
    Check if a value is a valid UUID.
    """
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False
