from . import db # Import the db object from the app package



class Task(db.model):
    id = db.Column(db.Integer, primary_key=True) # Create a column called id which is an integer and is the primary key
    title = db.Column(db.String, nullable=False) # Create a column called title which is a string and cannot be null
    description = db.Column(db.String, nullable=False) # Create a column called description which is a string and cannot be null
    completed = db.Column(db.Boolean, default=False) # Create a column called completed which is a boolean and defaults to False
    createdAt = db.Column(db.DateTime, default=datetime.utcnow) # Create a column called createdAt which is a datetime and defaults to the current time
    dueDate = db.Column(db.DateTime) # Create a column called dueDate which is a datetime and can be null
    