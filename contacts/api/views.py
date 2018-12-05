from flask import Blueprint
from flask_restful import Api

from contacts.api.resources import (
    RecordsResource,
    RecordResource
)


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(RecordResource, '/contacts/<cid>')
api.add_resource(RecordsResource, '/contacts')
