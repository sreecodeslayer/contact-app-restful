from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required
from flask import jsonify, request, make_response
from sqlalchemy import exc

from ...models import Records
from ...schemas import RecordSchema
from ...extensions import db
from ...helpers.paginator import paginate


class RecordResource(Resource):

    method_decorators = [jwt_required]

    def get(self, rid):
        schema = RecordSchema()
        curruser = get_current_user()
        rec = curruser.contacts.filter_by(id=rid).first_or_404()
        return schema.jsonify(rec)

    def patch(self, rid):
        schema = RecordSchema(partial=True)
        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)
        _, errors = schema.load(request.json)
        if errors:
            return errors, 422

        curruser = get_current_user()
        rec = curruser.contacts.filter_by(id=rid).first_or_404()
        name = request.json.get('name')
        if name:
            rec.name = name
        surname = request.json.get('surname')
        rec.surname = surname
        mobile = request.json.get('mobile')
        if mobile:
            rec.mobile = mobile

        db.session.add(rec)
        try:
            db.session.commit()
        except exc.IntegrityError:
            return make_response(
                jsonify(msg='A contact exists for that email'), 409)
        return schema.jsonify(rec)

    def delete(self, rid):
        schema = RecordSchema()
        curruser = get_current_user()
        rec = curruser.contacts.filter_by(id=rid).first_or_404()
        db.session.delete(rec)
        db.session.commit()
        return jsonify(msg='Contact removed')


class RecordsResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = RecordSchema(many=True)
        curruser = get_current_user()
        recs = curruser.contacts
        return paginate(recs, schema)

    def post(self):
        schema = RecordSchema()
        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)
        rec, errors = schema.load(request.json)
        if errors:
            return errors, 422

        curruser = get_current_user()
        rec.user = curruser
        db.session.add(rec)
        try:
            db.session.commit()
        except exc.IntegrityError:
            return make_response(
                jsonify(msg='A contact exists for that email'), 409)
        return schema.jsonify(rec)
