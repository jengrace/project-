"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


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


@app.route('/login')
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

    if db.session.query(User).filter(User.email == "entered_username").one() != 0:
        user = User.user_id
        db_password = db.session.query(User).filter(Use)
        if entered_password ==
    else:
        pass # create account 


    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
