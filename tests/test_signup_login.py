import unittest
from contacts.app import create_app
from contacts.extensions import db
from contacts.models import Users


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_and_login(self):
        # register a new account
        response = self.client.post('/auth/signup', json={
            'email': 'test@example.com',
            'username': 'test',
            'passwd_digest': 'testpass',
        })
        self.assertEqual(response.status_code, 200)

        # Cases of Login

        # login with the new account
        response = self.client.post('/auth/login', json={
            'username': 'test',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)

        # login with invalid creds
        response = self.client.post('/auth/login', json={
            'username': 'test1',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/auth/login', json={
            'username': 'test',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get('msg'), 'User creds invalid')
