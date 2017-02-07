"""Movie Ratings."""

from jinja2 import StrictUndefined
import sqlalchemy
from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/login')
def login_form():
    """Show login page."""

    return render_template("login_page.html")


@app.route('/handle-login', methods=['POST'])
def login_process():
    """Redirect to homepage after login."""

    # get username and pw from login form
    # query database for existence of username
    # if username exists, get matching password
        # compare database password to entered password
        # redirect to homepage
    # if username doesn't exist:
        # create account and add user (and commit to DB)
        # redirect to homepage

    entered_username = request.form.get("username")
    entered_password = request.form.get("password")

    # Using try-except because .one() will return an error if the email is not
    # in the database. Except statement handles adding a new user.

    try:
        user = db.session.query(User).filter(User.email == entered_username).one()
    except sqlalchemy.orm.exc.NoResultFound:
        user = User(email=entered_username, password=entered_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Logged in as %s.' % entered_username)
        return redirect('/')

    if entered_password == user.password:
        session['current_user'] = entered_username
        flash('Logged in as %s' % entered_username)
        return redirect('/')
    else:
        flash('Incorrect username or password.')
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('current_user', None)
    flash('You have been logged out')
    return redirect('/login')


@app.route('/user-info')
def load_user_info():

    user = request.args.get('user_id')
    user_info = db.session.query(User.user_id,
                                 User.age,
                                 User.zipcode,
                                 Rating.movie_id).join(Rating).filter(User.user_id == user).first()

    rated_movies_obj = db.session.query(Rating.rating_id,
                                        Rating.score,
                                        Movie.title).join(Movie).filter(Rating.user_id == user).all()

    return render_template('user_details.html', user_info=user_info,
                                                rated_movies_obj=rated_movies_obj)


@app.route('/movies')
def movie_list():

    movies = Movie.query.order_by(Movie.title).all()

    return render_template('movies_list.html', movies=movies)


@app.route('/movie-info')
def load_movie_info():

    movie = request.args.get('movie_id')
    movie_info = db.session.query(Movie.title).filter(Movie.movie_id == movie).one()

    return render_template('movies_details.html', movie_info=movie_info)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(port=5000, host='0.0.0.0')
