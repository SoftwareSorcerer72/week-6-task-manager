from flask import Flask # Import the Flask class from the flask module
from flask_sqlalchemy import SQLAlchemy # Import the SQLAlchemy class from the flask_sqlalchemy module
from flask_migrate import Migrate # Import the Migrate class from the flask_migrate module
from config import Config # Import the Config class from the config module
from flask_jwt_extended import JWTManager # Import the JWTManager class from the flask_jwt_extended module
from flask_cors import CORS # Import the CORS class from the flask_cors module


app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5000") # Create a new Flask app
app.config.from_object(Config)  # Set the configuration from the Config class

app.config['JWT_SECRET_KEY'] = '123456789abc'  # Change this!
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models