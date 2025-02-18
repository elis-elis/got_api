from app import db


class House(db.Model):
    """
    Represents a house in the database. Each house has a unique name.
    Characters can belong to a house. Houses are stored separately
    to enforce data integrity and avoid redundancy.

    Attributes:
        id (int): The unique identifier for each house.
        name (str): The name of the house, must be unique.
    """
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    characters = db.relationship("Character", back_populates="house")

    def __repr__(self):
        """
        Returns a string representation of the House object.
        """
        return f"<House {self.name}>"


class Strength(db.Model):
    """
    Represents a strength in the database. Each strength has a unique description.
    Characters can have a particular strength.

    Attributes:
        id (int): The unique identifier for each strength.
        description (str): The description of the strength, must be unique.
    """
    __tablename__ = "strengths"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False, unique=True)

    characters = db.relationship("Character", back_populates="strength")

    def __repr__(self):
        """
        Returns a string representation of the Strength object.
        """
        return f"<Strength {self.description}>"


class Character(db.Model):
    """
    Represents a character in the database. Each character has a unique name
    and is associated with a house and a strength. This table maintains character-specific details.

    Attributes:
        id (int): The unique identifier for each character.
        name (str): The name of the character, must be unique.
        house_id (int): The foreign key linking to the associated House.
        animal (str): The character's associated animal (if any).
        symbol (str): The character's associated symbol (if any).
        nickname (str): The character's nickname (if any).
        role (str): The character's role or occupation.
        age (int): The character's age (if applicable).
        death (int): The year the character died (if applicable).
        strength_id (int): The foreign key linking to the associated Strength.
    """
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=True)
    animal = db.Column(db.String(50), nullable=True)
    symbol = db.Column(db.String(50), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)
    strength_id = db.Column(db.Integer, db.ForeignKey("strengths.id"), nullable=False)

    house = db.relationship("House", back_populates="characters")
    strength = db.relationship("Strength", back_populates="characters")

    def to_dict(self):
        """
        Convert the Character object to a dictionary, including related models.
        Directly accesses self.house.id, which can raise an AttributeError if house is None.
        Instead of "house": None, it's better to return an empty dictionary {}.

        Returns:
            dict: A dictionary representation of the Character object with nested house and strength information.
        """
        return {
            "id": self.id,
            "name": self.name,
            "house": {"id": self.house.id, "name": self.house.name} if self.house else {},
            "animal": self.animal,
            "symbol": self.symbol,
            "nickname": self.nickname,
            "role": self.role,
            "age": self.age,
            "death": self.death,
            "strength": {"id": self.strength.id, "description": self.strength.description} if self.strength else {},
        }

    def __repr__(self):
        """
        Returns a string representation of the Character object.
        """
        # method helps in debugging by providing a string representation
        return f"<Character {self.name}>"
