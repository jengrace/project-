"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Admin(db.Model):
    """Administrators of admin site."""

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(70), nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.shelter_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Admin admin_id=%s email=%s username %s password %s>" % (
                                                                self.admin_id,
                                                                self.email,
                                                                self.username,
                                                                self.password
                                                                )


class Animal(db.Model):
    """ Animals on rescue website. """

    __tablename__ = "animals"

    animal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #born_at = db.Column(db.DateTime, nullable=False) #integer or string? format of date? datetime?
    img_url = db.Column(db.String(300), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    breed = db.Column(db.String(40), nullable=True)
    name = db.Column(db.String(40), nullable=True)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.shelter_id'), nullable=False)
    #timestamp

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Animal animal_id=%s img_url=%s gender=%s breed=%s name=%s>" % (
                                                                self.animal_id,
                                                                self.img_url,
                                                                self.gender,
                                                                self.breed,
                                                                self.name)


class Shelter(db.Model):
    """ Shelters on rescue website"""

    __tablename__ = "shelters"

    shelter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Shelter shelter_id=%s name=%s phone=%s location=%s>" % (
                                                                self.shelter_id,
                                                                self.name,
                                                                self.phone,
                                                                self.location)


class User(db.Model):
    """ User of rescue site """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s password=%s zipcode=%s>" % (
                                                                self.user_id,
                                                                self.email,
                                                                self.password,
                                                                self.zipcode)


class ShelterUser(db.Model):
    """ Ratings on ratings website. """

    __tablename__ = "shelter_users"

    su_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelters.shelter_id'), nullable=False)

    # Defining relationships with other tables:
    user = db.relationship("User", backref=db.backref("shelter_users"))
    shelter = db.relationship("Shelter", backref=db.backref("shelter_users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s movie_id=%s user_id=%s>" % (
                                                                self.rating_id,
                                                                self.movie_id,
                                                                self.user_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
