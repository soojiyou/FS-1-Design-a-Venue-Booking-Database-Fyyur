import os
from flask import Flask
from flask_moment import Moment

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

SQLALCHEMY_DATABASE_URI = 'postgres://sjofxezngemthe:01e4bbe6276660d0f7b0c5bb08542b8110d45cbcfc8b3d26fb28173f005a428a@ec2-52-54-200-216.compute-1.amazonaws.com:5432/d790t0rv3cfqhg'


# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/fyyur'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
