from flask import request, jsonify, Blueprint, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity
)

from contacts.models import Users
from contacts.schemas import UserSchema
from contacts.extensions import pwd_context, jwt, db
from sqlalchemy import exc

# from mongoengine.errors import NotUniqueError

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/login', methods=['POST'])
def login():
    '''Authenticate user and return token
    '''
    if not request.is_json:
        return make_response(
            jsonify(msg='Missing JSON in request'), 400)

    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return make_response(
            jsonify(msg='Missing username or password'), 400)

    user = Users.query.filter_by(username=username).first_or_404()
    if not pwd_context.verify(password, user.passwd_digest):
        return jsonify({'msg': 'User creds invalid'}), 400

    access_token = create_access_token(identity=str(user.id))
    return make_response(
        jsonify(access_token=access_token), 200)


@blueprint.route('/signup', methods=['POST'])
def signup():
    '''
    Add a new user to the platform
    '''
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), 400
    schema = UserSchema()

    user, errors = schema.load(request.json)
    if errors:
        return make_response(
            jsonify(errors), 422)
    user.passwd_digest = pwd_context.hash(
        user.passwd_digest)
    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError as e:
        return make_response(
            jsonify(msg='User exists with under that email/username'), 422)
    return schema.jsonify(user)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return Users.query.get(identity)
