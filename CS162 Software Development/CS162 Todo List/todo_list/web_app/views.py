# Import necessary libraries and modules
from . import db  # Database module from the current package
from .models import User, TodoItem  # Models for User and Todo items
from flask import Blueprint, request, jsonify  # Flask functionalities for route definition, request handling and JSON responses
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity  # JWT functionalities for authentication and user identification

# Define a Blueprint for all security related routes
security_bp = Blueprint('security', __name__)

@security_bp.route('/register', methods=['POST'])
def register():
    """Endpoint to register new users."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validate username and password presence
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "Username already exists"}), 400

    # Create a new user and add to the database
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201

@security_bp.route('/login', methods=['POST'])
def login():
    """Endpoint for users to login and receive an authentication token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check user credentials
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

def get_tasks_recursive(task):
    """Utility function to recursively serialize tasks and their subtasks."""
    return {
        "id": task.id,
        "content": task.content,
        "is_completed": task.is_completed,
        "parent_id": task.parent_id,
        "sub_items": [get_tasks_recursive(sub_task) for sub_task in task.sub_items]
    }

@security_bp.route('/get-tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Endpoint to retrieve all tasks for the authenticated user."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Fetch and serialize tasks for the user
    top_level_tasks = TodoItem.query.filter_by(user_id=current_user_id, parent_id=None).all()
    tasks_json = [get_tasks_recursive(task) for task in top_level_tasks]
    
    return jsonify({"tasks": tasks_json}), 200

@security_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    """Endpoint to add a new task for the authenticated user."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    new_task = TodoItem(content=data['content'], user_id=current_user_id)
    if 'parent_id' in data:
        new_task.parent_id = data['parent_id']
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully", "task_id": new_task.id}), 201

@security_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Endpoint to update a specific task's details for the authenticated user."""
    current_user_id = get_jwt_identity()
    task = TodoItem.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.get_json()

    # Update the task fields based on provided data
    if 'content' in data:
        task.content = data['content']
    if 'is_completed' in data:
        task.is_completed = data['is_completed']
    
    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200

@security_bp.route('/tasks/<int:task_id>/move', methods=['PUT'])
@jwt_required()
def move_task(task_id):
    """Endpoint to move a task under another task (parent task) for the authenticated user."""
    current_user_id = get_jwt_identity()
    task = TodoItem.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.get_json()
    new_parent_id = data.get('new_parent_id', None)

    # Validate the new parent task if provided
    if new_parent_id:
        parent_task = TodoItem.query.filter_by(id=new_parent_id, user_id=current_user_id).first()
        if not parent_task:
            return jsonify({"message": "Invalid parent task"}), 400

    # Move the task under the new parent
    task.parent_id = new_parent_id
    db.session.commit()

    return jsonify({"message": "Task moved successfully"}), 200

def gather_subtasks(task_id):
    """Recursive utility function to gather all subtask IDs for a given task."""
    ids_to_delete = [task_id]
    subtasks = TodoItem.query.filter_by(parent_id=task_id).all()
    for subtask in subtasks:
        ids_to_delete.extend(gather_subtasks(subtask.id))
    return ids_to_delete

@security_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Endpoint to delete a task and all its subtasks for the authenticated user."""
    current_user_id = get_jwt_identity()
    
    # Verify if the task to be deleted belongs to the current user
    task = TodoItem.query.filter_by(id=task_id, user_id=current_user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    # Gather all the subtask IDs recursively to ensure all related tasks are also deleted
    tasks_to_delete = gather_subtasks(task_id)

    # Perform batch deletion for efficiency
    TodoItem.query.filter(TodoItem.id.in_(tasks_to_delete)).delete(synchronize_session='fetch')
    
    db.session.commit()
    return jsonify({"message": "Task and its subtasks deleted successfully"}), 200