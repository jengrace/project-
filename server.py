"""Site for animal rescues to administer"""

import os
from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Rescue, Animal, Gender, Size, Age, Admin, connect_to_db, db
from sqlalchemy import func

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage. Displays list of rescues"""

    rescues = Rescue.query.all()

    admin = db.session.query(Admin.admin_id).first()

    return render_template('homepage.html',
                           rescues=rescues,
                           admin=admin)


@app.route('/<int:rescue_id>')
def load_rescue_info(rescue_id):
    """ Displays rescue details and list of available dogs & cats """

    rescue_info = db.session.query(Rescue.rescue_id,
                                   Rescue.name,
                                   Rescue.phone,
                                   Rescue.address,
                                   Rescue.email,
                                   Rescue.img_url).filter(Rescue.rescue_id == rescue_id).first()

    animals = db.session.query(Animal).filter(Animal.rescue_id == rescue_id).all()

    return render_template('rescue_info.html',
                           rescue_info=rescue_info,
                           animals=animals)


@app.route('/<int:rescue_id>/<int:animal_id>')
def load_animal_info(rescue_id, animal_id):

    animal_info = db.session.query(Animal.animal_id,
                                    Animal.img_url,
                                    Animal.name,
                                    Animal.rescue_id,
                                    Animal.gender_id,
                                    Gender.gender_name,
                                    Age.age_id,
                                    Age.age_category,
                                    Size.size_category).outerjoin(Gender, Age, Size).filter(Animal.animal_id == animal_id).first()
    print '^^^^^^^^^^^^^^^^^^^^^^^^ animal_info: ', animal_info

    return render_template('animal_info.html',
                            animal_info=animal_info)


@app.route('/admin/<int:admin_id>')
def load_admin_page(admin_id):
    """ Show admin page """

    admin = db.session.query(Admin.admin_id,
                             Admin.email,
                             Admin.password,
                             Admin.rescue_id).filter(Admin.admin_id == admin_id).first()

    # checks if a logged in admin exists and making sure that only the logged in admin only sees the admin page that belongs to them
    if 'current_admin' not in session or admin.email != session['current_admin']:
        return redirect('/')
    else:
        return render_template('admin_page.html',
                                admin=admin)


# For a given file, return whether it's an allowed file or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route that will process the file upload and other form input data
@app.route('/handle-add-animal', methods=['GET', 'POST'])
def add_animal_process():
    """ Sends admins form input to the database """

    admin = db.session.query(Admin.admin_id).filter(Admin.email == session['current_admin']).first()
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/admin/' + str(admin.admin_id))
        # Get the name of the uploaded file
        uploaded_file = request.files['file']
        # If user does not select a file, browser also
        # submits an empty part without filename
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect('/admin/' + str(admin.admin_id))
        # Check if the file is one of the allowed types/extensions
        if uploaded_file and allowed_file(uploaded_file.filename):
            name = request.form.get("name").title()
            gender = request.form.get("gender")
            age = request.form.get("age")
            size = request.form.get("size")
            #species = request.form.get("species").title()

            gender = db.session.query(Gender.gender_id).filter(Gender.gender_name == gender).first()
            age = db.session.query(Age.age_id).filter(Age.age_category == age).first()
            size = db.session.query(Size.size_id).filter(Size.size_category == size).first()
            rescue = db.session.query(Rescue).join(Admin).filter(Admin.email == session['current_admin']).first()
            user_filename = uploaded_file.filename
            # Store the extension of uploaded file to add to user_filename
            extension = user_filename.rsplit('.', 1)[1].lower()
            # Get the next animal id to add to user_filename
            result = db.session.query(func.max(Animal.animal_id)).one()
            next_animal_id = str(result[0] + 1)
            # Create file name based on rescue + animal ids
            user_filename = str(rescue.rescue_id) + '-' + next_animal_id + '.' + extension
            # Move the file from the temporal folder to the upload folder that was set up
            path = os.path.join(app.config['UPLOAD_FOLDER'], user_filename)
            uploaded_file.save(path)


            # Creating an instance (row) in the animals table
            animal = Animal(name=name, rescue=rescue, img_url=path,
                            gender_id=gender, age_id=age, size_id=size)
            print '&&&&&&&&&&&&&&&&&&&&&&: animal: ', animal
            # Adding the animal instance to the animals table

            db.session.add(animal)

            db.session.commit()

    return redirect('/' + str(rescue.rescue_id))


@app.route('/admin-login')
def admin_login_form():
    """ Show login page for admins only. """

    return render_template("admin_login_page.html")


@app.route('/handle-admin-login', methods=['POST'])
def process_admin_login():
    """ Redirect to admin page after login. """

    entered_email = request.form.get("email")
    entered_password = request.form.get("password")

    #admin = db.session.query(Admin).filter(Admin.email == entered_email).one()
    #print '******************* admin: ', admin.email
    try:
        admin = db.session.query(Admin).filter(Admin.email == entered_email).one()
    except:
        flash('Could not locate your account. Please click on sign up to create an account!')
        return redirect('/')
    #     admin = Admin(email=entered_email, password=entered_password)
    #     db.session.add(admin)
    #     db.session.commit()
    #     ad_id = db.session.query(Admin.admin_id).filter(Admin.admin_id == admin.admin_id).one()
    #     ad_id = ad_id[0]
    #     flash('Account created. Logged in as %s.' % entered_email)
    #     return redirect('/admin' + '/' + str(ad_id))
    if entered_password == admin.password:
        session['current_admin'] = entered_email
        ad_id = db.session.query(Admin.admin_id).filter(Admin.admin_id == admin.admin_id).one()
        ad_id = ad_id[0]
        flash('Logged in as %s' % entered_email)
        return redirect('/admin' + '/' + str(ad_id))
    else:
        flash('Incorrect password. Please try logging in again.')
        return redirect('/')


@app.route('/admin-logout')
def admin_logout():
    session.pop('current_admin', None)
    flash('You have been logged out')
    return redirect('/')


@app.route('/admin-signup')
def admin_signup():
    #flash('Thanks for signing up! Will be in contact shortly!')
    return render_template("signup_page.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # File uploads
    UPLOAD_FOLDER = 'static/images/'
    # These are the extensions accepting to be uploaded
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    # This is the path to the upload directory
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.run(port=5000, host='0.0.0.0')
