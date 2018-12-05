import unittest
from contacts.app import create_app
from contacts.extensions import db
from contacts.models import Users, Records
from flask_jwt_extended import create_access_token


class ContactApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.baseURL = '/api/v1'

        # Create a test user
        usr = Users(
            email='test@example.com',
            username='test'
        )
        usr.set_password('testpass')
        db.session.add(usr)
        db.session.commit()
        self.user = usr

        # Setup a bearer token
        with self.app_context:
            self.token = create_access_token(self.user.id)

    def get_auth_headers(self):
        hdr = {'Authorization': f'Bearer {self.token}'}
        return hdr

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_bad_auth(self):
        # send bad auth based requests
        response = self.client.get(self.baseURL + '/contacts')
        self.assertEqual(response.status_code, 401)

        response = self.client.post(self.baseURL + '/contacts', json={})
        self.assertEqual(response.status_code, 401)

        response = self.client.get(self.baseURL + '/contacts/1')
        self.assertEqual(response.status_code, 401)

        response = self.client.patch(self.baseURL + '/contacts/1', json={})
        self.assertEqual(response.status_code, 401)

        response = self.client.delete(self.baseURL + '/contacts/1')
        self.assertEqual(response.status_code, 401)

    def test_contacts_get(self):
        # send a GET req for contacts list
        response = self.client.get(
            self.baseURL + '/contacts',
            headers=self.get_auth_headers()
        )
        self.assertEqual(response.status_code, 200)

    def test_contacts_crud_integration(self):

        payload = {
            'name': 'Test Name',
            'surname': 'Test Surname',
            'email': 'test@example.com',
            'mobile': '+910123456789'
        }

        response = self.client.post(
            self.baseURL + '/contacts',
            json=payload,
            headers=self.get_auth_headers()
        )

        self.assertEqual(response.status_code, 200)
        # Assert response is equal to patch payload
        self.assertEqual(
            response.json.get('name'),
            payload.get('name')
        )
        self.assertEqual(
            response.json.get('surname'),
            payload.get('surname')
        )
        self.assertEqual(
            response.json.get('email'),
            payload.get('email')
        )
        self.assertEqual(
            response.json.get('mobile'),
            payload.get('mobile')
        )

        recid = response.json.get('id')

        # GET THE CONTACT
        response = self.client.get(
            self.baseURL + f'/contacts/{recid}',
            headers=self.get_auth_headers()
        )
        contact = response.json
        self.assertEqual(response.status_code, 200)
        # Assert response is equal to get payload
        self.assertEqual(
            contact.get('name'),
            payload.get('name')
        )
        self.assertEqual(
            contact.get('surname'),
            payload.get('surname')
        )
        self.assertEqual(
            contact.get('email'),
            payload.get('email')
        )
        self.assertEqual(
            contact.get('mobile'),
            payload.get('mobile')
        )

        # PATCH THE CONTACT
        patch_payload = {
            'name': 'Test Name - Patched',
            'surname': 'Test Surname - Patched',
            'mobile': '+910123456780'
        }

        response = self.client.patch(
            self.baseURL + f'/contacts/{recid}',
            json=patch_payload,
            headers=self.get_auth_headers()
        )

        contact = response.json
        self.assertEqual(response.status_code, 200)
        # Assert response is equal to patch payload
        self.assertEqual(
            contact.get('name'),
            patch_payload.get('name')
        )
        self.assertEqual(
            contact.get('surname'),
            patch_payload.get('surname')
        )
        self.assertEqual(
            contact.get('mobile'),
            patch_payload.get('mobile')
        )

        # DELETE THE CONTACT
        response = self.client.delete(
            self.baseURL + f'/contacts/{recid}',
            headers=self.get_auth_headers()
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('msg'), 'Contact removed')

        # CONFIRM THERE IS 404 AFTER DELETE
        response = self.client.get(
            self.baseURL + f'/contacts/{recid}',
            headers=self.get_auth_headers()
        )
        self.assertEqual(response.status_code, 404)
