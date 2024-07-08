from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_bcrypt import Bcrypt
 
db = SQLAlchemy()
bcrypt = Bcrypt()
 
 
class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    # serialize_rules = ("-_password_hash",)  # Exclude password_hash from serialization
 
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    
 
    def __repl__(self):
        return f'user{self.username} , id{self.id}'
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
 
    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
 
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Corrected 'User' to match table name
    user = db.relationship('User', backref=db.backref('entries', lazy=True))
