# Import necessary libraries and modules
from . import db  # Database module from the current package
from flask import current_app  # To get the current Flask app instance
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing and verification

# Define User model
class User(db.Model):
    # Primary key column
    id = db.Column(db.Integer, primary_key=True)
    
    # Column for storing usernames; ensures usernames are unique and cannot be null
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Column for storing hashed passwords
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Define a relationship between User and TodoItem; this allows retrieval of all items for a user
    items = db.relationship('TodoItem', backref='user', lazy=True)

    # Method to hash and set the password for the user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check if the provided password matches the hashed password of the user
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define TodoItem model
class TodoItem(db.Model):
    # Primary key column
    id = db.Column(db.Integer, primary_key=True)
    
    # Column for storing the content of the todo item
    content = db.Column(db.String(300), nullable=False)
    
    # Column to check if a todo item is completed; defaults to False
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Optional foreign key to denote sub-tasks or related tasks within TodoItem
    parent_id = db.Column(db.Integer, db.ForeignKey('todo_item.id'), nullable=True)
    
    # Foreign key column linking each todo item to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Define a relationship for potential sub-items within the TodoItem itself
    sub_items = db.relationship('TodoItem', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

# This block is executed if this script is run directly (not imported)
if __name__ == "__main__":
    # Create all tables defined in the models
    with current_app.app_context():
        db.create_all()