from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Model definitions

class Species(db.Model):
    """ Types of animals on rescue page """

    __tablename__ = 'species'

    species_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    species_type = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Species species_id=%s species_type=%s' % (self.species_id,
                                                           self.species_type)


class Breed(db.Model):
    """ Types of breeds for the admin to choose from """

    __tablename__ = 'breeds'

    breed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breed_type = db.Column(db.String(50), nullable=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.species_id'), nullable=True)

    species = db.relationship('Species', backref=db.backref("breeds", order_by=breed_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Species breed_id=%s breed_type=%s species_id=%s' % (self.breed_id,
                                                                     self.breed_type,
                                                                     self.species_id)


class Gender(db.Model):
    """ Gender of animals on rescue page"""

    __tablename__ = 'genders'

    gender_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    gender_type = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Gender gender_id=%s gender_category=%s' % (self.gender_id,
                                                            self.gender_type)


class Age(db.Model):
    """ Age of animals on rescue page """

    __tablename__ = 'ages'

    age_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    age_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Age age_id=%s age_category=%s' % (self.age_id,
                                                   self.age_category)


class Size(db.Model):
    """ Size of animals on rescue page """

    __tablename__ = 'sizes'

    size_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    size_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Size size_id=%s size_category=%s' % (self.size_id,
                                                      self.size_category)


class Rescue(db.Model):
    """ Animal rescues on rescue website """

    __tablename__ = 'rescues'

    rescue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    img_url = db.Column(db.String(300), nullable=True, default='static/images/GPR.png')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Rescue rescue_id=%s name=%s>' % (self.rescue_id,
                                                  self.name)


class Admin(db.Model):
    """Administrators of admin site."""

    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    rescue_id = db.Column(db.Integer, db.ForeignKey('rescues.rescue_id'), nullable=True)  # just a number, not an object!

    def __repr__(self):
        """Provide helpful representation when printed."""

        return '<Admin admin_id=%s rescue_id=%s>' % (self.admin_id,
                                                     self.rescue_id)

    rescue = db.relationship('Rescue', backref=db.backref("admins", order_by=admin_id))


class Animal(db.Model):
    """ Animals on rescue website. """

    __tablename__ = 'animals'

    animal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    img_url = db.Column(db.String(300), nullable=True, default='static/images/dog.png')
    name = db.Column(db.String(40), nullable=True)
    bio = db.Column(db.Text, nullable=True, default='Loving and very sweet. Looking for furever home!')
    is_adopted = db.Column(db.Boolean, nullable=True, default=False)  # will be a True or False
    is_visible = db.Column(db.Boolean, nullable=True, default=True)  # will be a True or False
    rescue_id = db.Column(db.Integer, db.ForeignKey('rescues.rescue_id'), nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.gender_id'), nullable=True)
    age_id = db.Column(db.Integer, db.ForeignKey('ages.age_id'), nullable=True)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.size_id'), nullable=True)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'), nullable=True)

    # Defining relationships
    # point to the Rescue class and load multiple of those. backref is a simple way to declare a new property on the Rescue class
    rescue = db.relationship('Rescue', backref=db.backref("animals", order_by=animal_id))
    gender = db.relationship('Gender', backref=db.backref("animals", order_by=animal_id))
    age = db.relationship('Age', backref=db.backref("animals", order_by=animal_id))
    size = db.relationship('Size', backref=db.backref("animals", order_by=animal_id))
    breed = db.relationship('Breed', backref=db.backref("animals", order_by=animal_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return '<Animal animal_id=%s name=%s>' % (self.animal_id,
                                                  self.name)




##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///project'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
