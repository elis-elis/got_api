from sqlalchemy.exc import SQLAlchemyError
from app import db, handle_sqlalchemy_error


def safe_commit():
    """
    Commits the current DB session and rolls back if an error occurs.
    """
    try:
        db.session.commit()
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return handle_sqlalchemy_error(db_error)


def get_total_count(model):
    """
    Returns the total count of records (rows) for a given SQLAlchemy model.

    Let’s say you want to get the total count of all characters in your Character table.
    Instead of writing db.session.query(Character).count() each time, use the get_total_count function.
    total_characters = get_total_count(Character)
    """
    return db.session.query(model).count()
