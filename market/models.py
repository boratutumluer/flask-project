from market import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin  # for these errors, 'User' object has no attribute 'is_active', is_authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=1024), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    # For insert into database
    def __init__(self, username, email_address, password):
        self.username = username
        self.email_address = email_address
        self.password = generate_password_hash(password)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=500), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=100), nullable=False, unique=True)
    description = db.Column(db.String(length=10000), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))




