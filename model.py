"""Models and database functions for HB project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Species(db.Model):
    """ Types of animals on rescue page """

    __tablename__ = "species"

    species_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Species species_id=%s species=%s" % (self.species_id,
                                                      self.species)


class Gender(db.Model):
    """ Gender of animals on rescue page"""

    __tablename__ = "genders"

    gender_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    gender_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Gender gender_id=%s gender_category=%s" % (self.gender_id,
                                                            self.gender_name)


class Age(db.Model):
    """ Age of animals on rescue page """

    __tablename__ = "ages"

    age_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    age_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Age age_id=%s age_category=%s" % (self.age_id,
                                                   self.age_category)


class Size(db.Model):
    """ Size of animals on rescue page """

    __tablename__ = "sizes"

    size_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    size_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Size size_id=%s size_category=%s" % (self.size_id,
                                                      self.size_category)


class Rescue(db.Model):
    """ Animal rescues on rescue website """

    __tablename__ = "rescues"

    rescue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    img_url = db.Column(db.String(300), nullable=True, default='static/images/GPR.png')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rescue rescue_id=%s name=%s phone=%s " + \
               "address=%s> email=%s img_url=%s" % (self.rescue_id,
                                                    self.name,
                                                    self.phone,
                                                    self.address,
                                                    self.email,
                                                    self.img_url)


class Admin(db.Model):
    """Administrators of admin site."""

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    rescue_id = db.Column(db.Integer, db.ForeignKey('rescues.rescue_id'), nullable=True)  # just a number, not an object!

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Admin admin_id=%s email=%s" + \
               "password=%s rescue_id=%s>" % (self.admin_id,
                                              self.email,
                                              self.password,
                                              self.rescue_id)

    rescue = db.relationship('Rescue', backref=db.backref("admins", order_by=admin_id))


class Animal(db.Model):
    """ Animals on rescue website. """

    __tablename__ = "animals"

    animal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    img_url = db.Column(db.String(300), nullable=True, default='static/images/dog.png')
    breed = db.Column(db.String(40), nullable=True)
    name = db.Column(db.String(40), nullable=True)
    rescue_id = db.Column(db.Integer, db.ForeignKey('rescues.rescue_id'), nullable=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'), nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.gender_id'), nullable=True)
    age_id = db.Column(db.Integer, db.ForeignKey('ages.age_id'), nullable=True)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.size_id'), nullable=True)

    # Defining relationships
    rescue = db.relationship('Rescue', backref=db.backref("animals", order_by=animal_id))
    species = db.relationship('Species', backref=db.backref("animals", order_by=animal_id))
    gender = db.relationship('Gender', backref=db.backref("animals", order_by=animal_id))
    age = db.relationship('Age', backref=db.backref("animals", order_by=animal_id))
    size = db.relationship('Size', backref=db.backref("animals", order_by=animal_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Animal animal_id=%s img_url=%s name=%s gender_id=%s>" % (self.animal_id,
                                                                             self.img_url,
                                                                             #self.breed,
                                                                             self.name,
                                                                             #self.rescue_id,
                                                                             #self.animal_type_id,
                                                                             self.gender_id)
                                                                             #self.age_id,
                                                                             #self.size_id)


class User(db.Model):
    """ User of rescue site """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s password=%s " + \
               "zipcode=%s>" % (self.user_id,
                                self.email,
                                self.password,
                                self.zipcode)


class RescueUser(db.Model):
    """ Ratings on ratings website. """

    __tablename__ = "rescue_users"

    su_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rescue_id = db.Column(db.Integer, db.ForeignKey('rescues.rescue_id'), nullable=False)

    # Defining relationships with other tables:
    #user = db.relationship("User", backref=db.backref("shelter_users"))
    #shelter = db.relationship("Shelter", backref=db.backref("shelter_users"))


    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s>" % (
    #                                                             self.rating_id,
    #                                                             self.movie_id,
    #                                                             self.user_id)

# class Transaction(db.Model):
#     """ Redirecting users to PayPal to allow donations for rescues """

#     trans_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     amount = db.Column(db.Integet, nullable=False)
#     pay_pal_token =
#     user_id = 
#     shelter_id = 
#     donated_at = db.Column(db.DateTime, nullable=False)

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
    db.create_all()
    print "Connected to DB."
