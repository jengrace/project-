"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
#from datetime import datetime
from model import Admin, Animal, Rescue, Age, Gender, Size, AnimalType, User
#from model import Animal
#from model import Rescue
#from model import Age, Gen

from model import connect_to_db, db
from server import app


def load_admins():
    """Load admins from u.admin into database."""

    print "Administrators"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    #Admin.query.delete()

    # Read u.admin file and insert data
    for row in open("seed_data/u.admin"):
        row = row.rstrip()
        admin_id, email, password, rescue_id = row.split("|")

        admin = Admin(admin_id=admin_id,
                      email=email,
                      password=password,
                      rescue_id=rescue_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(admin)

    # Once we're done, we should commit our work
    db.session.commit()


def load_rescues():
    """Load rescues from u.rescue into database."""

    print "Rescues"

    for row in open('seed_data/u.rescue'):
        row = row.rstrip()
        rescue_id, name, phone, address, email = row.split("|")

        rescue = Rescue(rescue_id=rescue_id,
                        name=name,
                        phone=phone,
                        address=address,
                        email=email)

        db.session.add(rescue)

    db.session.commit()


# def load_animals():
#     """Load animals from u.animal into database."""

#     print "Animals"

#     for row in open("seed_data/u.animal"):
#         row = row.rstrip()
#         print 'row: ', row
#         animal_id, img_url, breed, name, rescue_id, animal_type_id, gender_id, age_id, size_id = row.split("|")
#         animal = Animal(animal_id=animal_id,
#                         #age=age,
#                         #img_url=img_url,
#                         gender=gender,
#                         breed=breed,
#                         name=name,
#                         rescue_id=rescue_id)

#         # Converting release_date string to a datetime object

#         # if released_str:
#         #     released_at = datetime.strptime(released_str, "%d-%b-%Y")
#         # else:
#         #     released_at = None

#         db.session.add(animal)

#     db.session.commit()

def load_animals():
    """Load animals from u.animal into database."""

    print "Animals"

    for row in open("seed_data/u.animal"):
        row = row.rstrip()
        animal_id, breed, name, rescue_id, animal_type_id, gender_id, age_id, size_id = row.split("|")
        animal = Animal(animal_id=animal_id,
                        breed=breed,
                        name=name,
                        rescue_id=rescue_id,
                        animal_type_id=animal_type_id,
                        gender_id=gender_id,
                        age_id=age_id,
                        size_id=size_id)

        # Converting release_date string to a datetime object

        # if released_str:
        #     released_at = datetime.strptime(released_str, "%d-%b-%Y")
        # else:
        #     released_at = None

        db.session.add(animal)

    db.session.commit()


def load_ages():
    """Load ages from u.age into database."""

    print "Ages"

    for row in open('seed_data/u.age'):
        row = row.rstrip()
        age_id, age_category = row.split("|")

        age = Age(age_id=age_id,
                  age_category=age_category)

        db.session.add(age)

    db.session.commit()


def load_genders():
    """Load genders from u.gender into database."""

    print "Genders"

    for row in open('seed_data/u.gender'):
        row = row.rstrip()
        gender_id, gender_name = row.split("|")

        gender = Gender(gender_id=gender_id,
                        gender_name=gender_name)

        db.session.add(gender)

    db.session.commit()


def load_sizes():
    """Load sizes from u.size into database."""

    print "Sizes"

    for row in open('seed_data/u.size'):
        row = row.rstrip()
        size_id, size_category = row.split("|")

        size = Size(size_id=size_id,
                    size_category=size_category)

        db.session.add(size)

    db.session.commit()


def load_animal_type():
    """ Load animal types from u.animal_type """

    print "Animal Types"

    for row in open('seed_data/u.animal_type'):
        row = row.rstrip()
        animal_type_id, animal_type = row.split("|")

        animal_type = AnimalType(animal_type_id=animal_type_id,
                                 animal_type=animal_type)

        db.session.add(animal_type)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Admin.admin_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('admins_admin_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    #db.session.close()
    db.drop_all()

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_animal_type()
    load_ages()
    load_genders()
    load_sizes()
    load_rescues()
    load_animals()
    load_admins()

    set_val_user_id()
