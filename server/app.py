# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Example SQLite URI, replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Used for session management, replace with a secure key

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login or JWT for authentication

# Import your models
from models import User, JournalEntry

if __name__ == '__main__':
    app.run(debug=True)
