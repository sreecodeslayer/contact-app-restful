from marshmallow import (
    fields,
    validate,
    post_load
)

from contacts.extensions import ma
from contacts.models import Users


class UserSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    username = ma.String(required=True)
    email = ma.String(
        required=True, validate=validate.Email(
            error='Not a valid email address')
    )
    passwd_digest = ma.String(load_only=True, required=True)
    joined_on = ma.DateTime(dump_only=True)

    @post_load
    def make_user(self, data):
        return Users(**data)
