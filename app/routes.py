from flask import request, render_template
from . import app
from datetime import datetime
from fake_data.tasks import tasks_list


# Define a route
@app.route("/")
def index():
    greeting= 'Hello there! Welcome to the To Do API'
    return greeting


# task Endpoints

# Get All Posts
@app.route('/task')
def get_tasks():
    # Get the tasks from storage 
    task = tasks_list 
    return task

   
# Get a Single Task By ID
@app.route('/task/<int:task_id>')
def get_task(task_id):
    # Get the tasks from storage
    tasks = tasks_list
    # For each dictionary in the list of task dictionaries
    for task in tasks:
        # If the key of 'id' matches the task_id from the URL
        if task['id'] == task_id:
            # Return that task dictionary
            return task
    # If we loop through all of the tasks without returning, the task with that ID does not exist
    return {'error': f"task with an ID of {task_id} does not exist"}, 404


@app.route('/task', methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields =[]
    for fields in required_fields:
        if fields not in data:
            missing_fields.append(fields)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in your request body"}, 400
    
    title = data['title']
    description = data['description']

    new_task = {
        'id': len(tasks_list) + 1,
        'title': title,
        'description': description,
        'completed': False,
        'createdAt': datetime.now(datetime.UTC),
        'dueDate': data.get('dueDate')
    }




    return data 