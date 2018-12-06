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

    def test_search_contact(self):
        cat = Records(
            name='Cat',
            surname='Cat',
            email='cat@animals.com',
            mobile='+911123456789'
        )
        cat.user = self.user
        dog = Records(
            name='Dog',
            surname='Dog',
            email='dog@animals.com',
            mobile='+912123456789'
        )
        dog.user = self.user
        snake = Records(
            name='Snake',
            surname='Snake',
            email='snake@reptiles.com',
            mobile='+913123456789'
        )
        snake.user = self.user
        db.session.add(cat)
        db.session.add(dog)
        db.session.add(snake)

        db.session.commit()

        # Predominantly search name field
        catq = Records.query.filter(
            (Records.name.contains('cat')) | (
                Records.email.contains('cat')
            )
        )
        self.assertListEqual(list(catq), [cat])

        dogq = Records.query.filter(
            (Records.name.contains('dog')) | (
                Records.email.contains('dog')
            )
        )
        self.assertListEqual(list(dogq), [dog])

        snakeq = Records.query.filter(
            (Records.name.contains('snake')) | (
                Records.email.contains('snake')
            )
        )
        self.assertListEqual(list(snakeq), [snake])

        # Predominantly search email field
        animalsq = Records.query.filter(
            (Records.name.contains('animals')) | (
                Records.email.contains('animals')
            )
        )
        self.assertListEqual(list(animalsq), [cat, dog])

        reptilesq = Records.query.filter(
            (Records.name.contains('reptiles')) | (
                Records.email.contains('reptiles')
            )
        )
        self.assertListEqual(list(reptilesq), [snake])
