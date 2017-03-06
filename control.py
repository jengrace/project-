import sqlalchemy
import model as m
import os


def get_rescue(rescue_id):
    """ Get rescue details
    Input: id(int) of a rescue from the rescues table
    Output: Rescue model object
    """

    return m.db.session.query(m.Rescue).filter(
        m.Rescue.rescue_id == rescue_id).first()


def get_animal(animal_id):
    """ Get animal details
    Input: id(int) of an animal from the animals table
    Output: Animal model object
    """

    return m.db.session.query(m.Animal.animal_id, m.Animal.img_url,
                              m.Animal.name, m.Animal.rescue_id,
                              m.Animal.gender_id, m.Animal.bio,
                              m.Gender.gender_type, m.Age.age_id,
                              m.Age.age_category, m.Size.size_category,
                              m.Breed.breed_type).outerjoin(
                              m.Gender, m.Age, m.Size,
                              m.Breed).filter(
                              m.Animal.animal_id == animal_id).first()


def get_available_animals(rescue_id):
    """ Get animals that are currently available for adoption
    Input: id(int) of a rescue from the rescues table
    Output: List of Animal model objects
    """

    return m.db.session.query(m.Animal).filter(
        m.Animal.rescue_id == rescue_id, m.Animal.is_adopted == 'f', m.Animal.is_visible == 't').limit(10).all()


def get_admin_by_id(admin_id):
    """ Get admin by id
    Input: id(int) of an admin from the admins table
    Output: Admin model object
    """

    return m.db.session.query(m.Admin).filter(
        m.Admin.admin_id == admin_id).first()


def get_admin_by_session(email):
    """ Get admin of currently logged in admin
    Input: email(string) of logged in admin user from the session
    Output: Admin model object
    """

    return m.db.session.query(m.Admin).filter(m.Admin.email == email).first()


def allowed_file(filename, ALLOWED_EXTENSIONS):
    """ Return whether the file is an allowed file or not
    Inputs: filename of uploaded file(string), set of strings
    Output: True or False
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_animal(admin_request, admin_session, upload_folder):
    """ Add new animal to the database
    Inputs: request object, session dictionary, upload directory path(string)
    Output: Rescue model object that belongs to the logged in admin user to use
    for the URL redirect route.
    """

    name = admin_request.form.get('name').title()
    gender = admin_request.form.get('gender')
    age = admin_request.form.get('age')
    size = admin_request.form.get('size')
    breed = admin_request.form.get('breeds')
    bio = admin_request.form.get('bio')
    is_adopted = admin_request.form.get('is_adopted')
    is_visible = admin_request.form.get('is_visible')

    gender_id = m.db.session.query(m.Gender.gender_id).filter(
        m.Gender.gender_type == gender).first()
    age_id = m.db.session.query(m.Age.age_id).filter(
        m.Age.age_category == age).first()
    size_id = m.db.session.query(m.Size.size_id).filter(
        m.Size.size_category == size).first()
    breed_id = m.db.session.query(m.Breed.breed_id).filter(
        m.Breed.breed_type == breed).first()

    # return the rescue that belongs to the logged in admin, func will be returning this!
    rescue = m.db.session.query(m.Rescue).join(m.Admin).filter(
        m.Admin.email == admin_session['current_admin']).first()

    # temporary filename
    user_filename = admin_request.files['file'].filename
    # Store the extension of uploaded file to add to user_filename
    extension = user_filename.rsplit('.', 1)[1].lower()

    animal = m.Animal(name=name, rescue=rescue,
                      gender_id=gender_id, age_id=age_id, size_id=size_id,
                      breed_id=breed_id, bio=bio, is_adopted=is_adopted,
                      is_visible=is_visible)

    # Adding the animal instance to the animals table
    m.db.session.add(animal)
    m.db.session.commit()

    # animal id of animal just added to db
    a_id = animal.animal_id

    # rename filename
    user_filename = str(rescue.rescue_id) + '-' + str(a_id) + '.' + extension
    path = os.path.join(upload_folder, user_filename)
    admin_request.files['file'].save(path)

    animal.img_url = path
    m.db.session.commit()

    return rescue


def add_rescue(admin_request, admin_session, upload_folder):
    """ Add new rescue to the database
    Inputs: request object, session dictionary, path to the upload directory(string)
    Output: Rescue model object
    """

    rescue_name = admin_request.form.get('rescuename').title()
    phone = admin_request.form.get('phone')
    address = admin_request.form.get('address')
    email = admin_request.form.get('email')

    # temporary filename
    user_filename = admin_request.files['file'].filename
    # storing the extension of uploaded file
    extension = user_filename.rsplit('.', 1)[1].lower()

    # setting up the population with new data from form input to the rescue table
    rescue = m.Rescue(name=rescue_name, phone=phone, address=address,
                      email=email)

    # adding new instance/row to the rescue table
    m.db.session.add(rescue)
    # commit the new instance
    m.db.session.commit()

    # getting rescue_id of rescue that was just commited
    r_id = rescue.rescue_id

    # Create file name based on the rescue's id
    user_filename = str(r_id) + '.' + extension
    # Move the file from the temporal folder to the upload folder that was set up
    path = os.path.join(upload_folder, user_filename)
    # Saving the file to the upload folder
    admin_request.files['file'].save(path)

    # Updating the rescues table with rescue's image url
    rescue.img_url = path
    m.db.session.commit()

    return rescue


def update_admin_row(admin, rescue):
    """ Update row of admin table with rescue_id of newly added rescue
    Inputs: Admin model object, Rescue model object
    Output: No output, just updates a row in the admin table
    """

    admin.rescue_id = rescue.rescue_id
    m.db.session.commit()


def get_last_rescue_added():
    """ Get last rescue object added to the db
    Output: Resue model object
    """

    last_rescue_id_added = m.db.session.query(sqlalchemy.func.max(
        m.Rescue.rescue_id)).one()
    last_rescue_id_added = last_rescue_id_added[0]
    last_rescue = get_rescue(last_rescue_id_added)

    return last_rescue


def get_last_admin_added():
    """ Get last admin object added to the db
    Output: Admin model object
    """

    last_admin_id_added = m.db.session.query(sqlalchemy.func.max(
        m.Admin.admin_id)).one()
    last_admin_id_added = last_admin_id_added[0]
    last_admin = get_admin_by_id(last_admin_id_added)

    return last_admin


def get_admin(email, password):
    """ Check if admin user exists , returns admin or False
    Inputs: email(string), password(string) from HTML form
    Output: Admin model object OR False
    """

    try:
        admin = m.db.session.query(m.Admin).filter(
            m.Admin.email == email).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return False
    if password == admin.password:
        return admin
    else:
        return False
