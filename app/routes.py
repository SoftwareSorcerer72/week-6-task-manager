from flask import request, render_template, jsonify
from . import app
from datetime import datetime
from .models import User, Task
from app import db
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])     # Define a route for the /tasks/<task_id> endpoint with the GET method
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {'error': f"Task with ID {task_id} does not exist"}, 404
    return jsonify(task.to_dict())

@app.route('/tasks', methods=['POST'])   # Define a route for the /tasks endpoint with the POST method
@jwt_required()
def create_task():
    if not request.is_json:
        return {'error': 'Content type must be application/json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in your request body"}, 400
    new_task = Task(title=data['title'], description=data['description'], user_id=get_jwt_identity())
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])     # Define a route for the /tasks/<task_id> endpoint with the PUT method
@jwt_required()
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {'error': f"Task with ID {task_id} does not exist"}, 404
    if task.user_id != get_jwt_identity():
        return {'error': 'Unauthorized'}, 403
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])  # Define a route for the /tasks/<task_id> endpoint with the DELETE method
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {'error': f"Task with ID {task_id} does not exist"}, 404
    if task.user_id != get_jwt_identity():
        return {'error': 'Unauthorized'}, 403
    db.session.delete(task)
    db.session.commit()
    return {}, 204

@app.route('/users', methods=['POST'])      # Define a route for the /users endpoint with the POST method
def create_user():
    data = request.get_json()
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])     # Define a route for the /users/<user_id> endpoint with the GET method
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {'error': f"User with ID {user_id} does not exist"}, 404
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['PUT'])     # Define a route for the /users/<user_id> endpoint with the PUT method
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {'error': f"User with ID {user_id} does not exist"}, 404
    if user.id != get_jwt_identity():
        return {'error': 'Unauthorized'}, 403
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])  # Define a route for the /users/<user_id> endpoint with the DELETE method
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {'error': f"User with ID {user_id} does not exist"}, 404
    if user.id != get_jwt_identity():
        return {'error': 'Unauthorized'}, 403
    db.session.delete(user)
    db.session.commit()
    return {}, 204

@app.route('/token', methods=['GET'])   # Define a route for the /token endpoint with the GET method
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {'error': 'Basic auth required'}, 401
    user = User.query.filter_by(username=auth.username).first()
    if user is None or not user.check_password(auth.password):
        return {'error': 'Invalid username or password'}, 401
    return {'token': create_access_token(identity=user.id)}

@app.route('/me', methods=['GET'])  # Define a route for the /me endpoint with the GET method
@jwt_required()
def get_me():
    user = User.query.get(get_jwt_identity())
    return jsonify(user.to_dict())