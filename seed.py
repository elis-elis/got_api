import os
import json
from app import db, create_app
from app.models.character_model import Character, House, Strength


# Initialize the app and database
app = create_app()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory (data/)
DATA_FILE = os.path.join(BASE_DIR, "data", "characters.json")  # Construct path


def seed_database():
    """
    This function:
    - Loads character data from `data/characters.json`
    - Ensures that duplicate records are not inserted
    - Adds new characters to the database
    - Commits the transaction

    The function runs within an application context to allow database operations.
    """
    with app.app_context():
        try:
            with open(DATA_FILE, "r") as file:
                characters = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading character data: {e}")
            return

        # Insert houses and strengths if they don't already exist
        for character_data in characters:
            # Check if house already exists
            house_name = character_data.get("house")
            house = House.query.filter_by(name=house_name).first() if house_name else None
            if not house and house_name:
                house = House(name=house_name)
                db.session.add(house)
                print(f"Inserting House: {house_name} → ID: {house.id if house else 'NEW'}")
                db.session.flush()  # Get the ID before committing

            # Check if strength already exists
            strength_description = character_data.get("strength")
            strength = Strength.query.filter_by(description=strength_description).first() if strength_description else None
            if not strength and strength_description:
                strength = Strength(description=strength_description)
                db.session.add(strength)
                print(f"Inserting Strength: {strength_description} → ID: {strength.id if strength else 'NEW'}")
                db.session.flush()

            # Check if character already exists
            # If the query finds a match, existing_character will be an object; otherwise, it will be None
            existing_character = Character.query.filter_by(name=character_data["name"]).first()
            if not existing_character:
                character = Character(
                    name=character_data["name"],
                    house=house,
                    animal=character_data.get("animal"),
                    symbol=character_data.get("symbol"),
                    nickname=character_data.get("nickname"),
                    role=character_data["role"],
                    age=character_data.get("age"),
                    death=character_data.get("death"),
                    strength=strength
                )
                db.session.add(character)
        try:
            db.session.commit()
            print("Lovely! Database successfully added!")
        except Exception as e:
            db.session.rollback()  # Roll back any partial inserts
            print(f"Database error: {e}")


if __name__ == "__main__":
    """
    Runs the seeding script when executed directly.
    This ensures the function is only called when the script is run as a standalone program.
    """
    seed_database()
