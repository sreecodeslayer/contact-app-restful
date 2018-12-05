from marshmallow import (
    fields,
    validate,
    post_load
)

from contacts.extensions import ma
from contacts.models import Records


class RecordSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    name = ma.String(required=True)
    surname = ma.String()
    email = ma.String(
        required=True, validate=validate.Email(
            error='Not a valid email address')
    )
    mobile = ma.String()
    created_on = ma.DateTime(dump_only=True)

    @post_load
    def make_record(self, data):
        return Records(**data)
