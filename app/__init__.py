from flask import Flask # Import the Flask Class from the Flask module
from flask_sqlalchemy import SQLAlchemy # Import the SQLAlchemy Class from the flask_sqlalchemy module
from flask_migrate import Migrate # Import the Migrate Class from the flask_migrate module
from config import Config # Import the Config class from the config module

# Create an instance of Flask called app which will be the central object
app = Flask(__name__)
app.config.from_object(Config) # Set the database URI


db = SQLAlchemy(app) # Create an instance of the SQLAlchemy class called db
migrate = Migrate(app, db) # Create an instance of the Migrate class called migrate

# import the routes to the app
from . import routes
