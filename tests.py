import unittest
from server import app
from model import db, connect_to_db
import seed as s
import control as c


class RoutesTests(unittest.TestCase):
    """Tests Flask routes"""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, 'postgresql:///testdb')

        # drop all tables, if any
        db.drop_all()

        # Create tables and add sample data
        db.create_all()

        s.load_all()

    def test_homepage(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2> Animal Rescues </h2>', result.data)

    def test_rescue_page(self):
        rescue = c.get_rescue(1)
        rescue_id = str(rescue.rescue_id)
        result = self.client.get('/rescue/' + rescue_id)
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2> Adopt a Pet: </h2>', result.data)

    def test_animal_details_page(self):
        animal = c.get_animal(1)
        animal_id = str(animal.animal_id)
        rescue = c.get_rescue(1)
        rescue_id = str(rescue.rescue_id)
        result = self.client.get('/rescue/' + rescue_id + '/animal/' + animal_id)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Name: Archie', result.data)

    def test_login_page(self):
        result = self.client.get('/admin-login')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Email: ', result.data)

    def test_signup_page(self):
        result = self.client.get('/admin-signup')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Please contact ', result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()

        db.drop_all()


class LoggedUserTests(unittest.TestCase):
    """Tests pages that require log in"""

    def setUp(self):
        """Do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # drop all tables, if any
        db.drop_all()

        # Create tables and add sample data
        db.create_all()

        s.load_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()

        db.drop_all()

    def test_admin_page(self):
        """Tests the admin page that allows animals to be added to their
        rescue page."""

        test_admin_email = 'test1@gmail.com'
        with self.client as cl:
            with cl.session_transaction() as sess:
                sess['current_admin'] = test_admin_email

        logged_in_admin = c.get_admin_by_session(test_admin_email)
        logged_in_admin_id = str(logged_in_admin.admin_id)
        result = self.client.get('/admin/' + logged_in_admin_id)

        # import pdb; pdb.set_trace()

        self.assertEqual(result.status_code, 200)
        self.assertIn('<b>Please provide information for each animal: </b>', result.data)

    def test_add_rescue_page(self):
        """Tests the admin page that allows a new admin user to add a rescue
        to my page."""

        test_admin_email = 'test5@gmail.com'
        with self.client as cl:
            with cl.session_transaction() as sess:
                sess['current_admin'] = test_admin_email

        logged_in_admin = c.get_admin_by_session(test_admin_email)
        logged_in_admin_id = str(logged_in_admin.admin_id)

        result = self.client.get('/admin/' + logged_in_admin_id + '/rescue-info')
        self.assertEqual(result.status_code, 200)
        self.assertIn("<b>Please provide your rescue's information: </b>", result.data)

    def test_add_rescue_page_not_logged_in(self):
        """Tests the admin page redirects a non logged in user."""

        test_admin_email = 'test4@gmail.com'

        logged_in_admin = c.get_admin_by_session(test_admin_email)
        logged_in_admin_id = str(logged_in_admin.admin_id)

        result = self.client.get('/admin/' + logged_in_admin_id + '/rescue-info')
        self.assertEqual(result.status_code, 302)

    def test_admin_page_not_logged_in(self):
        """Tests the admin page redirects a non logged in user."""

        test_admin_email = 'test4@gmail.com'

        logged_in_admin = c.get_admin_by_session(test_admin_email)
        logged_in_admin_id = str(logged_in_admin.admin_id)

        result = self.client.get('/admin/' + logged_in_admin_id)
        self.assertEqual(result.status_code, 302)


class TestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # drop all tables, if any
        db.drop_all()

        # Create tables and add sample data
        db.create_all()

        s.load_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()

        db.drop_all()

    def test_fetch_rescue(self):
        """Tests retrieving the correct rescue according to its id"""

        rescue = c.get_rescue(2)
        assert rescue.rescue_id == 2
        assert rescue.name == 'Alachua County Animal Services'

    def test_fetch_animal(self):
        """Tests retrieving the correct animal according to its id"""

        animal = c.get_animal(1)
        assert animal.animal_id == 1
        assert animal.name == 'Archie'

    def test_available_animals(self):
        """Tests retrieving only animals available for adoption per rescue
        filtered by rescue id"""

        available_animals = c.get_available_animals(1)
        assert len(available_animals) == 1

    def test_fetch_admin(self):
        """Tests retrieving the correct admin according to its id"""

        admin = c.get_admin_by_id(1)
        assert admin.admin_id == 1
        assert admin.email == 'test1@gmail.com'

    def test_existing_admin(self):
        """Tests for existing admins"""

        is_admin = c.get_admin('test1@gmail.com', '1234')
        assert is_admin.admin_id == 1

    def test_nonexisting_admin(self):
        """Tests that non existing admins are not able to log in"""

        is_admin = c.get_admin('test8@gmail.com', '8888')
        assert is_admin is False

    def test_last_admin(self):
        """Tests that the last admin added to the db is retrieved"""

        last_admin_added = c.get_last_admin_added()
        assert last_admin_added.admin_id == 6

    def test_last_rescue(self):
        """Tests that the last rescue added to the db is retrieved"""

        last_rescue_added = c.get_last_rescue_added()
        assert last_rescue_added.rescue_id == 5

if __name__ == "__main__":
    unittest.main()
