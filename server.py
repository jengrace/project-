from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Rescue, connect_to_db
import control as c
import sqlalchemy
import model as m
import os


app = Flask(__name__)

app.secret_key = 'ABC'

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage. Displays list of rescues"""

    title = 'My page'
    rescues = Rescue.query.all()

    return render_template('homepage.html',
                           rescues=rescues,
                           title=title)


@app.route('/rescue/<int:rescue_id>')
def load_rescue_info(rescue_id):
    """ Displays rescue details and list of available dogs & cats """

    rescue_info = c.get_rescue(rescue_id)
    title = rescue_info.name
    available_animals = c.get_available_animals(rescue_id)
    #available_animals = available_animals[:10]

    return render_template('rescue_info.html',
                           rescue_info=rescue_info,
                           available_animals=available_animals,
                           title=title)


@app.route('/rescue/<int:rescue_id>/animal/<int:animal_id>')
def load_animal_info(rescue_id, animal_id):
    """ Displays details of each animal """

    animal_info = c.get_animal(animal_id)
    title = animal_info.name

    return render_template('animal_info.html', animal_info=animal_info,
                           title=title)


@app.route('/admin/<int:admin_id>')
def load_admin_page(admin_id):
    """ Show admin page to add animals """

    title = 'Dashboard'
    admin = c.get_admin_by_id(admin_id)

    # redirects to homepage if user is not the logged in user
    if 'current_admin' not in session or admin.email != session['current_admin']:
        return redirect('/')
    else:
        return render_template('admin_page.html', admin=admin, title=title)


@app.route('/admin/<int:admin_id>/rescue-info')
def load_rescue_info_admin_page(admin_id):
    """ Show admin page to add a rescue """

    title = 'Dashboard'
    admin = c.get_admin_by_id(admin_id)

    # redirects to homepage if user is not the logged in user
    if 'current_admin' not in session or admin.email != session['current_admin']:
        return redirect('/')
    else:
        return render_template('rescue_info_admin.html', admin=admin,
                               title=title)


# Route that will process the file upload and other form input data
@app.route('/handle-add-animal', methods=['GET', 'POST'])
def add_animal_process():
    """ Sends admins form input to the database """

    email = session['current_admin']
    admin = c.get_admin_by_session(email)
    admin_id = admin.admin_id

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/admin/' + str(admin_id))
        # Get the name of the uploaded file
        uploaded_file = request.files['file']
        # If user does not select a file, browser also
        # submits an empty part without filename
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect('/admin/' + str(admin_id))
        # Check if the file is one of the allowed types/extensions
        if uploaded_file and c.allowed_file(uploaded_file.filename, ALLOWED_EXTENSIONS):
            # passing the request and session object
            animal = c.add_animal(request, session, app.config['UPLOAD_FOLDER'])

    return redirect('/rescue/' + str(animal.rescue_id))


@app.route('/handle-add-rescue', methods=['GET', 'POST'])
def add_rescue_process():
    """ Sends admins form input to the database """

    email = session['current_admin']
    admin = c.get_admin_by_session(email)
    admin_id = admin.admin_id

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/admin/' + str(admin_id) + '/rescue-info')
        # Get the name of the uploaded file
        uploaded_file = request.files['file']
        # If user does not select a file, browser also
        # submits an empty part without filename
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect('/admin/' + str(admin_id) + '/rescue-info')
        # Check if the file is one of the allowed types/extensions
        if uploaded_file and c.allowed_file(uploaded_file.filename, ALLOWED_EXTENSIONS):
            rescue = c.add_rescue(request, session, app.config['UPLOAD_FOLDER'])
            # Get admin object of currently logged in admin
            admin = c.get_admin_by_id(admin_id)
            # update admin row with its new rescue_id
            c.update_admin_row(admin, rescue)

    return redirect('/success')


@app.route('/success')
def add_rescue_success():
    """ Show login page for admins only. """

    title = 'Success'
    last_rescue = c.get_last_rescue_added()
    rescue_name = last_rescue.name
    rescue_id = last_rescue.rescue_id
    last_admin = c.get_last_admin_added()
    admin_id = last_admin.admin_id

    if 'current_admin' in session:
        return render_template("success_rescue_add.html",
                               last_rescue_added=rescue_id,
                               last_admin_added=admin_id,
                               rescue_name=rescue_name,
                               title=title)
    else:
        return redirect('/')


@app.route('/admin-login')
def admin_login_form():
    """ Show login page for admins only. """

    title = 'Login'

    return render_template("admin_login_page.html",
                           title=title)


@app.route('/handle-admin-login', methods=['POST'])
def process_admin_login():
    """ Redirect to admin page after login. """

    entered_email = request.form.get("email")
    entered_password = request.form.get("password")
    admin = c.get_admin(entered_email, entered_password)

    if admin is False:
        flash('Invalid credentials. Please click on sign up to create an account!')
        return redirect('/')
    session['current_admin'] = entered_email
    ad_id = admin.admin_id
    flash('Logged in as %s' % entered_email)
    if admin.rescue_id is None:
        return redirect('/admin' + '/' + str(ad_id) + '/rescue-info')
    else:
        return redirect('/admin' + '/' + str(ad_id))


@app.route('/admin-logout')
def admin_logout():
    """ Logs out admin user """

    session.pop('current_admin', None)
    flash('You have been logged out')

    return redirect('/')


@app.route('/admin-signup')
def admin_signup():
    """ Sign up page for new admin user """

    title = 'Sign up'

    return render_template('signup_page.html',
                           title=title)


@app.route('/handle-loading')
def handle_dynamic_loading():
    rescue_id = request.args.get("rescueid")
    counter = int(request.args.get("counter"))
    o = 10 + (counter*10)  # offset(skip) this many
    animals = m.db.session.query(m.Animal).filter(
        m.Animal.rescue_id == rescue_id, m.Animal.is_adopted == 'f', m.Animal.is_visible == 't').limit(10).offset(o).all()
    my_html = ''
    for animal in animals:
        animal_id = animal.animal_id
        animal_img = animal.img_url
        a = '<br><a href = "/rescue/%s/animal/%s"><img alt="portrait" src = "/%s"></a><br>' % (rescue_id, animal_id, animal_img)
        my_html = my_html + a
    return my_html

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
