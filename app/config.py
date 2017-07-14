import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools/random-string-generator.php
SECRET_KEY = 'xLO@6!MPj8'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True

JWT_HEADER_TYPE = 'JWT'
