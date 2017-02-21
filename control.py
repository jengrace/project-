import model as m
import os

def get_rescue(rescue_id):
    """ Get rescue details """

    rescue_details = m.db.session.query(m.Rescue).filter(m.Rescue.rescue_id == rescue_id).first()

    return rescue_details


def get_animal(animal_id):
    """ Get animal details """

    animal_info = m.db.session.query(m.Animal.animal_id, m.Animal.img_url,
                                     m.Animal.name, m.Animal.rescue_id,
                                     m.Animal.gender_id, m.Animal.bio,
                                     m.Gender.gender_type, m.Age.age_id,
                                     m.Age.age_category, m.Size.size_category,
                                     m.Breed.breed_type).outerjoin(
                                     m.Gender, m.Age, m.Size,
                                     m.Breed).filter(m.Animal.animal_id == animal_id).first()

    return animal_info


def get_available_animals(rescue_id):
    """ Get animals that are currently available for adoption """

    available_animals = m.db.session.query(m.Animal).filter(m.Animal.rescue_id == rescue_id, m.Animal.is_adopted == 'f', m.Animal.is_visible == 't').all()

    return available_animals


def get_admin(admin_id):
    """ Get admin object by id """

    admin = m.db.session.query(m.Admin).filter(m.Admin.admin_id == admin_id).first()
    return admin


def get_admin_by_session(email):
    """ Get id of currently logged in """

    admin_id = m.db.session.query(m.Admin.admin_id).filter(m.Admin.email == email).first()
    return admin_id[0]


#def add_animal(admin_request, admin_session, uploaded_file, upload_folder):
def add_animal(admin_request, admin_session, uploaded_file, upload_folder):
    name = admin_request.form.get("name").title()
    gender = admin_request.form.get("gender")
    age = admin_request.form.get("age")
    size = admin_request.form.get("size")
    breed = admin_request.form.get("breeds")
    bio = admin_request.form.get("bio")
    is_adopted = admin_request.form.get("is_adopted")
    is_visible = admin_request.form.get("is_visible")


    gender = m.db.session.query(m.Gender.gender_id).filter(m.Gender.gender_type == gender).first()
    age = m.db.session.query(m.Age.age_id).filter(m.Age.age_category == age).first()
    size = m.db.session.query(m.Size.size_id).filter(m.Size.size_category == size).first()
    breed = m.db.session.query(m.Breed.breed_id).filter(m.Breed.breed_type == breed).first()

    rescue = m.db.session.query(m.Rescue).join(m.Admin).filter(m.Admin.email == admin_session['current_admin']).first()

    #user_filename = uploaded_file.filename
    user_filename = admin_request.files['file'].filename

    # Store the extension of uploaded file to add to user_filename
    extension = user_filename.rsplit('.', 1)[1].lower()

    animal = m.Animal(name=name, rescue=rescue,
                    gender_id=gender, age_id=age, size_id=size,
                    breed_id=breed, bio=bio, is_adopted=is_adopted,
                    is_visible=is_visible)

    # Adding the animal instance to the animals table
    m.db.session.add(animal)

    m.db.session.commit()

    a_id = animal.animal_id

    user_filename = str(rescue.rescue_id) + '-' + str(a_id) + '.' + extension

    path = os.path.join(upload_folder, user_filename)

    uploaded_file.save(path)

    animal.img_url = path

    m.db.session.commit()

    return rescue


# For a given file, return whether it's an allowed file or not
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#def handle_add_animal():

