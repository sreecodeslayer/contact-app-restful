import unittest
import time
from datetime import datetime
from contacts.app import create_app
from contacts.extensions import db
from contacts.models import Users


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = Users(username='cat')
        u.set_password('cat')

        self.assertTrue(u.passwd_digest is not None)

    def test_password_verification(self):
        u = Users(username='cat')
        u.set_password('cat')

        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_password_salts_are_random(self):
        u = Users(username='cat')
        u.set_password('cat')

        u2 = Users(username='cat')
        u2.set_password('cat')

        self.assertTrue(u.passwd_digest != u2.passwd_digest)

    def test_new_user(self):
        usr = Users(
            email='cat@animals.com',
            username='cat',
        )
        usr.set_password('cat')
        db.session.add(usr)
        db.session.commit()

        self.assertTrue(usr.username is not None)
        self.assertTrue(usr.email is not None)
        self.assertTrue(usr.passwd_digest is not None)
        self.assertTrue(isinstance(usr.joined_on, datetime))
