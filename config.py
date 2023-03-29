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

SQLALCHEMY_DATABASE_URI = 'postgresql://ugmqneixdnggll:68b59e32daabd81609276787159cf240f3dc80d37132e57527e972e40e3c962c@ec2-3-230-24-12.compute-1.amazonaws.com:5432/d5sljav4fnv13u'


# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/fyyur'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
