from flask import request, render_template
from . import app
from datetime import datetime
from .models import Task
from flask import jsonify
from app import db

# Define a route
@app.route("/")
def index():
    greeting= 'Hello there! Welcome to the To Do API'
    return greeting


# task Endpoints

# Get All Posts
@app.route('/task')
def get_tasks():
    tasks = Task.query.all()  # Get all tasks from the database
    return jsonify([task.to_dict() for task in tasks])  # Convert tasks to dictionaries and jsonify

   
# Get a Single Task By ID
@app.route('/task/<int:task_id>')
def get_task(task_id):
    task = Task.query.get(task_id)  # Get the task with the given id from the database
    if task is None:
        return {'error': f"task with an ID of {task_id} does not exist"}, 404
    return jsonify(task.to_dict())  # Convert task to dictionary and jsonify


@app.route('/task', methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields =[]
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in your request body"}, 400
    
    title = data['title']
    description = data['description']

    new_task = Task(title=title, description=description)  # Create a new Task object
    db.session.add(new_task)  # Add the new Task to the session
    db.session.commit()  # Commit the session to save the new Task to the database

    return jsonify(new_task.to_dict()), 201  # Return the new task as JSON

