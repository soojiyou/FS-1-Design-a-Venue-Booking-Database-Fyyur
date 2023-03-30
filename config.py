import os
from flask import Flask
from flask_moment import Moment


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to the database

app = Flask(__name__)

moment = Moment(app)
app.config.from_object('config')

# ENV = 'prod'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/fyyur'
#     app.config['SECRET_KEY'] = os.urandom(32)
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/fyyur'
