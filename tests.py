import unittest
from server import app
from flask import session
from model import db, connect_to_db
import seed as s
import control as c


class FlaskTests(unittest.TestCase):
    """Tests for my animal rescues site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app)
        #connect_to_db(app, 'postgresql:///testdb')

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

    # def test_admin_add_animal(self):
    #     loggedin_admin = c.get_admin_by_session(sess['current_admin'])
    #     loggedin_admin_id = str(loggedin_admin.admin_id)
    #     result = self.client.get('/admin/' + loggedin_admin_id)
    #     self.assertIn('<b>Please provide information for each animal: </b>', result.data)


class TestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""
    def setUp(self):
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

    def test_some_db_thing(self):
        """Some database test..."""

        rescue = c.get_rescue(2)
        assert rescue.rescue_id == 2
        assert rescue.name == 'Alachua County Animal Servies'

        animal = c.get_animal(1)
        assert animal.animal_id == 1
        assert animal.name == 'Archie'

        available_animals = c.get_available_animals(1)
        assert len(available_animals) == 1

        admin = c.get_admin_by_id(1)
        assert admin.admin_id == 1
        assert admin.email == 'test1@gmail.com'

        is_admin = c.get_admin('test1@gmail.com', '1234')
        assert is_admin.admin_id == 1

        is_admin = c.get_admin('test8@gmail.com', '8888')
        assert is_admin == False

        last_admin_added = c.get_last_admin_added()
        assert last_admin_added.admin_id == 5

        last_rescue_added = c.get_last_rescue_added()
        assert last_rescue_added.rescue_id == 5

if __name__ == "__main__":
    unittest.main()
