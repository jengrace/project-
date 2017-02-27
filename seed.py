"""Utility file to seed project database from mock rescue data in seed_data/"""

from model import Admin, Animal, Rescue, Age, Gender, Size, Species, Breed
from model import connect_to_db, db
from server import app


def load_admins():
    """Load admins from u.admin into database."""

    #print "Administrators"

    # Read u.admin file and insert data
    for row in open("seed_data/u.admin"):
        row = row.rstrip()
        admin_id, email, password, rescue_id = row.split("|")

        if rescue_id == '':
            rescue_id = None

        admin = Admin(email=email,
                      password=password,
                      rescue_id=rescue_id)

        db.session.add(admin)
    db.session.commit()


def load_rescues():
    """Load rescues from u.rescue into database."""

    #print "Rescues"

    for row in open('seed_data/u.rescue'):
        row = row.rstrip()
        rescue_id, name, phone, address, email = row.split("|")

        rescue = Rescue(name=name,
                        phone=phone,
                        address=address,
                        email=email)

        db.session.add(rescue)
    db.session.commit()


def load_animals():
    """Load animals from u.animal into database."""

    #print "Animals"

    for row in open("seed_data/u.animal"):
        row = row.rstrip()
        animal_id, name, rescue_id, gender_id, age_id, size_id, breed_id = row.split("|")
        animal = Animal(name=name,
                        rescue_id=rescue_id,
                        gender_id=gender_id,
                        age_id=age_id,
                        size_id=size_id,
                        breed_id=breed_id)

        db.session.add(animal)
    db.session.commit()


def load_ages():
    """Load ages from u.age into database."""

    #print "Ages"

    for row in open('seed_data/u.age'):
        row = row.rstrip()
        age_id, age_category = row.split("|")

        age = Age(age_category=age_category)

        db.session.add(age)
    db.session.commit()


def load_genders():
    """Load genders from u.gender into database."""

    #print "Genders"

    for row in open('seed_data/u.gender'):
        row = row.rstrip()
        gender_id, gender_type = row.split("|")

        gender = Gender(gender_type=gender_type)

        db.session.add(gender)
    db.session.commit()


def load_sizes():
    """Load sizes from u.size into database."""

    #print "Sizes"

    for row in open('seed_data/u.size'):
        row = row.rstrip()
        size_id, size_category = row.split("|")
        size = Size(size_category=size_category)

        db.session.add(size)
    db.session.commit()


def load_species():
    """ Load species from u.species """

    #print "Species"

    for row in open('seed_data/u.species'):
        row = row.rstrip()
        species_id, species_type = row.split("|")

        species = Species(species_type=species_type)

        db.session.add(species)
    db.session.commit()


def load_breeds():
    """ Load breeds from u.breeds """

    #print "Breeds"

    for row in open('seed_data/u.breeds'):
        row = row.rstrip()
        breed_id, breed_type, species_id = row.split("|")

        breed = Breed(breed_type=breed_type, species_id=species_id)

        db.session.add(breed)
    db.session.commit()


def load_all():
    # Import different types of data
    load_species()
    load_breeds()
    load_ages()
    load_genders()
    load_sizes()
    load_rescues()
    load_animals()
    load_admins()


if __name__ == "__main__":
    connect_to_db(app)

    db.drop_all()

    # In case tables haven't been created, create them
    db.create_all()

    load_all()
