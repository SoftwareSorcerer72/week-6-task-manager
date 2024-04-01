import os # Import the os module

basedir = os.path.abspath(os.path.dirname(__file__)) # Get the base directory of the current file

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # Set the database URI