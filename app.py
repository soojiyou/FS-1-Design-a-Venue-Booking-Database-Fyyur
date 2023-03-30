# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import json
from dateutil.parser import parse
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from models import setup_db, Venue, Artist, Show
from config import app
from sqlalchemy import distinct
# import arrow

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)

# migrate = Migrate(app, db)


db = SQLAlchemy(app)
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):

    if isinstance(value, str):
        date = parse(value)
    else:
        date = value
    return babel.dates.format_datetime(date, format, locale='en')


# app.jinja_env.filters['datetime'] = format_datetime


# def phone_validator(num):
#     parsed = phonenumbers.parse(num, "US")
#     if not phonenumbers.is_valid_number(parsed):
#         raise ValidationError('Must be a valid US phone number.')
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    app.jinja_env.filters['datetime'] = format_datetime

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        # TODO: replace with real venues data.
        #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        venue_res_data = []

        d1 = datetime.now()
        venue_places = db.session.query(
            distinct(Venue.city), Venue.state, Venue.name).all()

        # venue_places = db.session.query(
        #     Venue.city, Venue.state, Venue.name).all()
        for place in venue_places:
            city = place[0]
            state = place[1]
            result = Venue.query.filter(Venue.state == state).filter(
                Venue.city == city).all()
            venue_data = []
            for venue in result:
                venue_data.append({
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows': Show.query.filter(Show.start_time > d1).count()
                })
            venue_res_data.append({
                'city': city,
                'state': state,
                'venues': venue_data
            })

        return render_template('pages/venues.html',  areas=venue_res_data)

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        # res_data = []
        data = []
        search_term = request.form.get('search_term')
        # count = 0
        d1 = datetime.now()
        result = Venue.query.filter(
            Venue.name.ilike('%'+search_term+'%')).all()
        for item in result:
            # count += 1
            shows = Show.query.filter(
                Show.venue_id == item.id, Show.start_time > d1).count()
            data.append({
                "id": item.id,
                "name": item.name,
                "num_upcoming_shows": shows
            })
        res_data = {
            "count": len(result),
            "data": data
        }
        return render_template('pages/search_venues.html', results=res_data, search_term=request.form.get('search_term', ''))

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # TODO: replace with real venue data from the venues table, using venue_id
        # first(): return first value from selected item
        # with_entities(): Return a new Query replacing the SELECT list with the given entities.
        venue_data = Venue.query.get(venue_id)
        d1 = datetime.now()

        past_shows = []
        upcomming_shows = []
        past = Show.query.join(Artist, Show.artist_id == Artist.id).filter(
            Show.venue_id == venue_id).filter(Show.start_time <= d1).all()
        upcomming = Show.query.join(Artist, Show.artist_id == Artist.id).filter(
            Show.venue_id == venue_id).filter(Show.start_time > d1).all()
        for show in past:
            artist_id = show.artist_id

            # if show.start_time > d1:
            past_shows.append({
                "artist_id":  artist_id,
                "artist_name": Artist.query.get(artist_id).name,
                "artist_image_link":  Artist.query.get(artist_id).image_link,
                "start_time": format_datetime(str(show.start_time))
            })
            # if show.start_time < d1:
        for show in upcomming:
            artist_id = show.artist_id
            upcomming_shows.append({
                "artist_id":  artist_id,
                "artist_name": Artist.query.get(artist_id).name,
                "artist_image_link":  Artist.query.get(artist_id).image_link,
                "start_time": format_datetime(str(show.start_time))

            })

        data = {"id": venue_data.id,
                "name": venue_data.name,
                "genrse": venue_data.genres,
                "address": venue_data.address,
                "city": venue_data.city,
                "state": venue_data.state,
                "phone": venue_data.phone,
                "website": venue_data.website,
                "facebook_link": venue_data.facebook_link,
                "seeking_talent": venue_data.seeking_talent,
                "seeking_description": venue_data.seeking_description,
                "image_link": venue_data.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcomming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcomming_shows),
                }

        return render_template('pages/show_venue.html', venue=data)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        # error = False

        # TODO: insert form data as a new Venue record in the db, instead

        try:
            name = request.form.get('name')
            city = request.form.get('city')
            state = request.form.get('state')
            address = request.form.get('address')
            phone = request.form.get('phone')
            formated_phone = find_phone_numbers(phone)
            image_link = request.form.get('image_link')
            facebook_link = request.form.get('facebook_link')
            website = request.form.get('website_link')
            seeking_talent = True if request.form.get(
                'seeking_talent') == 'Yes' else False
            seeking_description = request.form.get('seeking_description')
            genres = request.form.getlist('genres')

            new_venue = Venue(name=name,
                              city=city,
                              state=state,
                              address=address,
                              phone=formated_phone,
                              image_link=image_link,
                              facebook_link=facebook_link,
                              website=website,
                              seeking_talent=seeking_talent,
                              seeking_description=seeking_description,
                              genres=genres)

            # TODO: modify data to be the data object returned from db insertion
            db.session.add(new_venue)
            db.session.commit()
            db.session.refresh(new_venue)
            # on successful db insert, flash success
            print(f'Venue ' + request.form['name'] +
                  ' was successfully listed!')
        except:
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            db.session.rollback()
            # error = True
            print(sys.exc_info())
            flash(
                "An error occurred. Venue "
                + request.form.get("name")
                + " could not be listed."
            )
        finally:
            db.session.close()
            return render_template('pages/home.html')
        # if error:
        #     abort(500)
        # else:
        #     return render_template('pages/home.html')

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        # TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
        # venue = db.session.query(Venue).get(venue_id)

        try:
            db.session.query(Venue).filter_by(id=venue_id).delete()
            db.session.commit()
        except:

            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

        return render_template('pages/home.html')
        # return jsonify({"redirect_to": url_for('search_venues')})
        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage

    #  Artists
    #  ----------------------------------------------------------------

    @app.route('/artists')
    def artists():
        # TODO: replace with real data returned from querying the database

        artist_res_data = []
        # artists_data = []
        artists = db.session.query(Artist).all()

        for artist in artists:
            artist_res_data.append({
                'id': artist.id,
                'name': artist.name
            })

        return render_template('pages/artists.html', artists=artist_res_data)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        # res_data = []
        data = []
        d1 = datetime.now()

        search_term = request.form.get('search_term')
        result = Artist.query.filter(
            Artist.name.ilike('%'+search_term+'%')).all()

        for item in result:
            shows = Show.query.filter(
                Show.artist_id == item.id, Show.start_time > d1).all()
            data.append({
                "id": item.id,
                "name": item.name,
                "num_upcoming_shows": len(shows)
            })
            res_data = {
                "count": len(data),
                "data": data
            }

        return render_template('pages/search_artists.html', results=res_data, search_term=request.form.get('search_term', ''))

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        # shows the artist page with the given artist_id
        # TODO: replace with real artist data from the artist table, using artist_id
        artist_data = Artist.query.get(artist_id)
        d1 = datetime.now()

        past_shows = []
        upcomming_shows = []

        past = Show.query.join(Venue, Show.venue_id == Venue.id).filter(
            Show.artist_id == artist_id).filter(Show.start_time <= d1).all()
        upcomming = Show.query.join(Venue, Show.venue_id == Venue.id).filter(
            Show.artist_id == artist_id).filter(Show.start_time > d1).all()

        for show in past:
            venue_id = show.venue_id

            # if show.start_time > d1:
            past_shows.append({
                "venue_id":  venue_id,
                "venue_name": Venue.query.get(venue_id).name,
                "venue_image_link":  Venue.query.get(venue_id).image_link,
                "start_time": format_datetime(str(show.start_time))
            })
            # if show.start_time < d1:
        for show in upcomming:
            venue_id = show.venue_id
            upcomming_shows.append({
                "venue_id":  venue_id,
                "venue_name": Venue.query.get(venue_id).name,
                "venue_image_link":  Venue.query.get(venue_id).image_link,
                "start_time": format_datetime(str(show.start_time))

            })

        data = {"id": artist_data.id,
                "name": artist_data.name,
                "genrse": artist_data.genres,
                "city": artist_data.city,
                "state": artist_data.state,
                "phone": artist_data.phone,
                "website": artist_data.website,
                "facebook_link": artist_data.facebook_link,
                "seeking_talent": artist_data.seeking_talent,
                "seeking_description": artist_data.seeking_description,
                "image_link": artist_data.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcomming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcomming_shows),
                }

        # data = list(filter(lambda d: d['id'] ==
        #             artist_id, [data1, data2, data3]))[0]
        return render_template('pages/show_artist.html', artist=data)

    #  Update
    #  ----------------------------------------------------------------

    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        try:
            artist_data = Artist.query.get(artist_id)
            artist = {}
            form = ArtistForm()
            artist = {"id": artist_data.id,
                      "name": artist_data.name,
                      "genrse": artist_data.genres,
                      "city": artist_data.city,
                      "state": artist_data.state,
                      "phone": artist_data.phone,
                      "website": artist_data.website,
                      "facebook_link": artist_data.facebook_link,
                      "seeking_talent": artist_data.seeking_talent,
                      "seeking_description": artist_data.seeking_description,
                      "image_link": artist_data.image_link,
                      }

        # TODO: populate form with fields from artist with ID <artist_id>
        except:
            print(sys.exc_info())
            flash("Something went wrong. Please try again.")
            return redirect(url_for("index"))
        finally:
            db.session.close()
        return render_template('forms/edit_artist.html', form=form, artist=artist)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes
        try:
            edited_artist = db.session.query(Artist).get(artist_id)

            phone = request.form.get('phone')
            formated_phone = find_phone_numbers(phone)

            edited_artist.name = request.form.get('name')
            edited_artist.city = request.form.get('city')
            edited_artist.state = request.form.get('state')
            edited_artist.phone = formated_phone
            edited_artist.image_link = request.form.get('image_link')
            edited_artist.facebook_link = request.form.get('facebook_link')
            edited_artist.website = request.form.get('website_link')
            edited_artist.seeking_talent = True if request.form.get(
                'seeking_talent') == 'Yes' else False
            edited_artist.seeking_description = request.form.get(
                'seeking_description')
            edited_artist.genres = request.form.getlist('genres')

            # TODO: modify data to be the data object returned from db insertion
            db.session.commit()

            print(f'Artist ' +
                  request.form['name'] + ' was successfully updated!')
        except:
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            db.session.rollback()
            # error = True
            print(sys.exc_info())
            flash(
                "An error occurred. Artist "
                + request.form.get("name")
                + " could not be updated."
            )
        finally:
            db.session.close()

        return redirect(url_for('show_artist', artist_id=artist_id))
        # return render_template('pages/show_artist.html', artist=edited_artist)

    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):

        try:
            venue_data = Venue.query.get(venue_id)
            venue = {}
            form = VenueForm()
            venue = {"id": venue_data.id,
                     "name": venue_data.name,
                     "genrse": venue_data.genres,
                     "address": venue_data.address,
                     "city": venue_data.city,
                     "state": venue_data.state,
                     "phone": venue_data.phone,
                     "website": venue_data.website,
                     "facebook_link": venue_data.facebook_link,
                     "seeking_talent": venue_data.seeking_talent,
                     "seeking_description": venue_data.seeking_description,
                     "image_link": venue_data.image_link,
                     }

        # TODO: populate form with values from venue with ID <venue_id>
        except:
            print(sys.exc_info())
            flash("Something went wrong. Please try again.")
            return redirect(url_for("index"))
        finally:
            db.session.close()

        return render_template('forms/edit_venue.html', form=form, venue=venue)

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):

        try:
            edited_venue = db.session.query(Venue).get(venue_id)
            phone = request.form.get('phone')
            formated_phone = find_phone_numbers(phone)
            edited_venue.name = request.form.get('name')
            edited_venue.city = request.form.get('city')
            edited_venue.state = request.form.get('state')
            edited_venue.address = request.form.get('address')
            edited_venue.phone = formated_phone
            edited_venue.image_link = request.form.get('image_link')
            edited_venue.facebook_link = request.form.get('facebook_link')
            edited_venue.website = request.form.get('website_link')
            edited_venue.seeking_talent = True if request.form.get(
                'seeking_talent') == 'Yes' else False
            edited_venue.seeking_description = request.form.get(
                'seeking_description')
            edited_venue.genres = request.form.getlist('genres')

            db.session.commit()
            print(f'Venue ' + request.form.get("name") +
                  ' was successfully updated!')
        except:
            # db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred. Venue "
                + request.form.get("name")
                + " could not be updated."
            )
        finally:
            db.session.close()
            return redirect(url_for('show_venue', venue_id=venue_id))
            # return render_template('pages/show_venue.html', venue=edited_venue)

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # TODO: insert form data as a new Venue record in the db, instead
        try:
            name = request.form.get('name')
            city = request.form.get('city')
            state = request.form.get('state')
            phone = request.form.get('phone')
            formated_phone = find_phone_numbers(phone)
            image_link = request.form.get('image_link')
            facebook_link = request.form.get('facebook_link')
            website = request.form.get('website_link')
            seeking_talent = True if request.form.get(
                'seeking_talent') == 'Yes' else False
            # seeking_talent = request.form.get('seeking_talent')
            seeking_description = request.form.get('seeking_description')
            genres = request.form.getlist('genres')

            new_artist = Artist(name=name,
                                city=city,
                                state=state,
                                phone=formated_phone,
                                image_link=image_link,
                                facebook_link=facebook_link,
                                website=website,
                                seeking_talent=seeking_talent,
                                seeking_description=seeking_description,
                                genres=genres)

        # TODO: modify data to be the data object returned from db insertion
            db.session.add(new_artist)
            db.session.commit()
            db.session.refresh(new_artist)
        # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        except:
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
            db.session.rollback()
            # error = True
            print(sys.exc_info())
            flash(
                "An error occurred. Artist "
                + request.form.get("name")
                + " could not be listed."
            )
        finally:
            db.session.close()
            return render_template('pages/home.html')

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        # TODO: replace with real venues data.

        show_res_data = []
        shows = db.session.query(Show).all()

        for show in shows:
            artist_id = show.artist_id
            venue_id = show.venue_id

            show_res_data.append({
                'venue_id': venue_id,
                'venue_name':  Venue.query.get(venue_id).name,
                'artist_id': artist_id,
                'artist_name': Artist.query.get(artist_id).name,
                'artist_image_link': Artist.query.get(artist_id).image_link,
                'start_time': format_datetime(str(show.start_time)),
            })

        return render_template('pages/shows.html', shows=show_res_data)

    @app.route('/shows/create', methods=['GET'])
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # TODO: insert form data as a new Show record in the db, instead

        try:
            form = ShowForm()
            artist_id = request.form.get('artist_id')
            venue_id = request.form.get('venue_id')
            start_time = request.form.get('start_time')

            availablity_artist = Artist.query.get(artist_id)
            availablity_venue = Venue.query.get(venue_id)

            if availablity_artist is None:
                flash(
                    "No artist with requested id "
                    + request.form.get("artist_id")
                )
            if availablity_venue is None:
                flash(
                    "No venue with requested id "
                    + request.form.get("venue_id")
                )
            else:
                new_show = Show(artist_id=artist_id,
                                venue_id=venue_id,
                                start_time=start_time)
            db.session.add(new_show)
            db.session.commit()
            db.session.refresh(new_show)
        # on successful db insert, flash success
            flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred. Show "
                + request.form.get("name")
                + " could not be listed."
            )
        finally:
            db.session.close()

        return render_template('pages/home.html')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#


# Default port:
# if __name__ == '__main__':
#     app.run()


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     APP.run(host='0.0.0.0', port=port)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
