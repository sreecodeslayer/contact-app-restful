import unittest
from datetime import datetime
from contacts.app import create_app
from contacts.extensions import db
from contacts.models import Users, Records


class ContactModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Create a test user
        usr = Users(
            email='test@example.com',
            username='test'
        )
        usr.set_password('testpass')
        db.session.add(usr)
        db.session.commit()
        self.user = usr

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_contact(self):
        rec = Records(
            name='Test Name',
            surname='Test Surname',
            email='test@example.com',
            mobile='+910123456789'
        )
        rec.user = self.user
        db.session.add(rec)
        db.session.commit()

        self.assertTrue(rec.name is not None)
        self.assertTrue(rec.surname is not None)
        self.assertTrue(rec.email is not None)
        self.assertTrue(rec.mobile is not None)
        self.assertTrue(rec.user is not None)
        self.assertTrue(isinstance(rec.created_on, datetime))
