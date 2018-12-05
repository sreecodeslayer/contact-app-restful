from ..extensions import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd_digest = db.Column(db.String(200), nullable=False)
    joined_on = db.Column(db.DateTime(), default=datetime.utcnow)

    # one to many for a users contact list
    contacts = db.relationship('Records', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return '(User : %r)' % self.username
