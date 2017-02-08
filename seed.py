"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from model import Admin
from model import Animal
from model import Shelter

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
        admin_id, email, password, shelter_id = row.split("|")

        admin = Admin(admin_id=admin_id,
                      email=email,
                      password=password,
                      shelter_id=shelter_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(admin)

    # Once we're done, we should commit our work
    db.session.commit()


def load_shelters():
    """Load shelters from u.shelter into database."""

    print "Shelters"

    #Shelter.query.delete()

    for row in open('seed_data/u.shelter'):
        row = row.rstrip()
        shelter_id, name, phone, address, email = row.split("|")

        shelter = Shelter(shelter_id=shelter_id,
                          name=name,
                          phone=phone,
                          address=address,
                          email=email)

        db.session.add(shelter)

    db.session.commit()


def load_animals():
    """Load animals from u.animal into database."""

    print "Animals"

    #Animal.query.delete()

    for row in open("seed_data/u.animal"):
        row = row.rstrip()
        print 'row: ', row
        animal_id, gender, breed, name, shelter_id = row.split("|")
        animal = Animal(animal_id=animal_id,
                        #age=age,
                        #img_url=img_url,
                        gender=gender,
                        breed=breed,
                        name=name,
                        shelter_id=shelter_id)

        # Converting release_date string to a datetime object

        # if released_str:
        #     released_at = datetime.strptime(released_str, "%d-%b-%Y")
        # else:
        #     released_at = None

        db.session.add(animal)

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

    db.drop_all()

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_shelters()
    load_admins()
    load_animals()
    set_val_user_id()
