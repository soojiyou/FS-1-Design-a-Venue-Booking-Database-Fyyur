from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from forms import *
from flask_migrate import Migrate
from config import app


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)

# # TODO: connect to a local postgresql database
# migrate = Migrate(app, db)

# # with app.app_context():
#     db.create_all()
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Unicode(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))

    def __repr__(self):
        venue_obj = {'venue_id': self.id, 'venue_name': self.name,
                     'city': self.city, 'state': self.state,
                     'address': self.address, 'phone': self.phone,
                     'image_link': self.image_link, 'facebook_link': self.facebook_link,
                     'website': self.website, 'seeking_talent': self.seeking_talent,
                     'seeking_description': self.seeking_description, 'genres': self.genres}
        return f'<{venue_obj}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Unicode(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String)

    def __repr__(self):
        artist_obj = {'artist_id': self.id, 'artist_name': self.name,
                      'city': self.city, 'state': self.state,
                      'phone': self.phone, 'image_link': self.image_link,
                      'facebook_link': self.facebook_link,
                      'website': self.website, 'seeking_talent': self.seeking_talent,
                      'seeking_description': self.seeking_description, 'genres': self.genres}
        return f'<{artist_obj}>'


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        show_obj = {'show_id': self.id, 'date': self.date,
                    'artist_id': self.artist_id, 'venue_id': self.venue_id,
                    'start_time': self.start_time, 'artist_image_link': self.aritst_image_link,
                    'artist_name': self.artist_name, 'venue_name': self.venue_name}
        return f'<{show_obj}>'
