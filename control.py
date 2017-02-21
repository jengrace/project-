import model as m


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
    """ Get admin by id """

    admin = m.db.session.query(m.Admin).filter(m.Admin.admin_id == admin_id).first()

    return admin
