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
