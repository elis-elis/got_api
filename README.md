
![Screenshot_of_grey_worm.png](Screenshot_of_grey_worm.png) 

# **Game of Thrones RESTful API (Flask & PostgreSQL)**

## **📌 Overview**
This project is a **Flask-based RESTful API** that interacts with a **PostgreSQL database**, representing a mock database of characters from *Game of Thrones*. It allows CRUD operations on characters and provides filtering, sorting, and pagination. The API supports both **database (PostgreSQL)** and **JSON-based storage** for character data.

---

## **📂 Project Structure**

📦 project-root ├── 📁 app │ ├── 📁 models # SQLAlchemy models │ ├── 📁 routes # Flask route handlers │ ├── 📁 services # Business logic (DB operations) │ ├── 📁 utils # Helper functions (filters, sorting, JSON handling) │ ├── init.py # Flask app initialization ├── 📄 config.py # Configuration settings ├── 📄 requirements.txt # Python dependencies ├── 📄 README.md # Project documentation

---

## **🚀 Features**
### **✅ Character Management**
- **Create, Read, Update, Delete (CRUD)**
- **Fetch characters from PostgreSQL**
- **Fetch characters from JSON storage**
- **Dynamic filtering, sorting, and pagination**

### **✅ Routes**
#### ** Database Routes**
| Method | Endpoint | Description |
|--------|-------------|-------------|
| **GET** | `/characters` | Get all characters with filters, sorting, pagination |
| **POST** | `/character` | Create a new character |
| **PATCH** | `/characters/<id>` | Update an existing character |
| **DELETE** | `/characters/<id>` | Delete a character |

#### ** JSON Routes**
| Method | Endpoint           | Description |
|--------|--------------------|-------------|
| **GET** | `/characters/json` | Get all characters from JSON (filters, sorting, pagination) |



---
####  **Tech Stack**
**Backend**: Flask, Flask-RESTful

**Database**: PostgreSQL, SQLAlchemy

**Authentication**: Flask-JWT-Extended

**Utilities**: Pydantic (for data validation)

---

## **🛠️ Setup & Installation**
### ** Prerequisites**
- **Python 3.8+**
- **PostgreSQL**
- **pip (Python package manager)**
- **Virtual environment (optional but recommended)**

### **Clone the Repository**
```bash
git clone <repository-url>
cd project-root

# Install Dependencies
pip install -r requirements.txt

# Set Up Database, Start PostgreSQL and create a database:
CREATE DATABASE got_characters;

# Set up environment variables (.env file):
DATABASE_URL=postgresql://username:password@localhost/got_characters
SECRET_KEY=your_secret_key

# Run database migrations:
flask db upgrade

# Run the Application
flask run

# API will be available at http://localhost:5000
