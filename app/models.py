from . import db # Import the db object from the app package
from datetime import datetime, timezone # Import the datetime and timezone classes from the datetime module


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Create a column called id which is an integer and is the primary key
    title = db.Column(db.String, nullable=False) # Create a column called title which is a string and cannot be null
    description = db.Column(db.String, nullable=False) # Create a column called description which is a string and cannot be null
    completed = db.Column(db.Boolean, nullable=False, default=False) # Create a column called completed which is a boolean and cannot be null and defaults to False
    createdAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # Create a column called createdAt which is a datetime and cannot be null and defaults to the current time in UTC
    dueDate = db.Column(db.DateTime) # Create a column called dueDate which is a datetime and can be null
