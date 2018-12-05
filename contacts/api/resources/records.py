from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required
from flask import jsonify, request, make_response
from ...models import Records
from ...schemas import RecordSchema
from ...extensions import db


class RecordResource(Resource):

    method_decorators = [jwt_required]

    def get(self, rid):
        schema = RecordSchema()
        curruser = get_current_user()
        rec = curruser.contacts.query.first_or_404(id=rid)
        return schema.jsonify(rec)

    def patch(self, rid):
        pass

    def delete(self, rid):
        pass


class RecordsResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = RecordSchema(many=True)
        pass

    def post(self):
        schema = RecordSchema()
        if not request.is_json:

            return make_response(
                jsonify(msg='Missing JSON in request'), 400)
        rec, errors = schema.load(request.json)
        if errors:
            return errors, 422
        db.session.add(rec)
        try:
            db.session.commit()
        except Exception as e:
            raise
        return schema.jsonify(rec)

    def delete(self):
        pass
