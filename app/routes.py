from flask import request
from . import app
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