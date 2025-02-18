import os
from dotenv import load_dotenv
import logging


# Load environment variables from .env
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_key")


def setup_logging():
    """
    Configures logging for the application.
    """
    logger = logging.getLogger()  # Get the root logger
    if not logger.hasHandlers():  # Prevent adding multiple handlers
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File Handler (logs to a file)
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler (logs to console)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
