from ..extensions import db
from datetime import datetime


class Records(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=True, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # one to many for a users contact list
    user = db.relationship(
        'Users', backref=db.backref('contacts', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Records, self).__init__(**kwargs)

    def __repr__(self):
        return '(Record : %r)' % self.name
