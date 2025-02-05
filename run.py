"""
Imports the create_app() function from app/__init__.py
Calls create_app() to initialize and configure Flask.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
