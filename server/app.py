import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_here')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from models import User, JournalEntry

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        username=data['username'],
        email=data['email'],
        password_hash=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.authenticate(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200

# Routes for CRUD operations
@app.route('/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    new_entry = JournalEntry(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        user_id=data['user_id']  # Assuming user_id is passed in the request data
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(message="Journal entry created successfully"), 201

@app.route('/entries', methods=['GET'])
def get_all_entries():
    entries = JournalEntry.query.all()
    return jsonify([{
        'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'category': entry.category,
        'date': entry.date,
        'user_id': entry.user_id
    } for entry in entries]), 200

@app.route('/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify(message="Journal entry not found"), 404
    return jsonify({
        'id': entry.id,
        'title': entry.title,
        'content': entry.content,
        'category': entry.category,
        'date': entry.date,
        'user_id': entry.user_id
    }), 200

@app.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify(message="Journal entry not found"), 404
    data = request.get_json()
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.category = data.get('category', entry.category)
    db.session.commit()
    return jsonify(message="Journal entry updated successfully"), 200

@app.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = JournalEntry.query.get(entry_id)
    if not entry:
        return jsonify(message="Journal entry not found"), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify(message="Journal entry deleted successfully"), 200

if __name__ == '__main__':
    app.run(debug=True)
