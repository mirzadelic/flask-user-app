from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import *

from logging import Formatter, FileHandler, INFO

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class UserApi(Resource):

    @jwt_required
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        return user.serialize()

    @jwt_required
    def put(self, user_id):
        data = request.json
        for field in User.required_fields:
            if field not in data:
                return {'msg': 'All fields are required.'}, 401

        if 'id' in data:
            del data['id']

        user = User.query.filter_by(id=user_id)
        user.update(data)
        user.first().password = data.get('password', None)
        db.session.commit()

        user = User.query.filter_by(id=user_id).first()
        return user.serialize()


class UserListApi(Resource):

    @jwt_required
    def get(self):
        users = User.query.all()
        return [user.serialize() for user in users]


@app.route('/api/login/', methods=['POST'])
def login():
    '''
    Params:
     - `email`
     - `password`

    Return object:
     - `token`
     - `user` object

    In client apps use JWT token with header, example:
    `Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c`
    '''
    data = request.json
    email = data.get('email', None)
    password = data.get('password', None)
    if email is None or password is None:
        return jsonify({'msg': 'Email and password are required fields.'}), 401

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({'msg': 'Bad username or password'}), 401

    return jsonify({'token': create_access_token(identity=user.email), 'user': user.serialize()}), 200


@app.route('/api/signup/', methods=['POST'])
def signup():
    '''
    Request params:
     - `first_name`
     - `last_name`
     - `email`
     - `password`

    Return created object:
     - `user` object
    '''
    data = request.json
    for field in User.required_fields:
        if field not in data:
            return jsonify({'msg': 'All fields are required fields.'}), 401

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'msg': 'User with email \'%s\' already exists.' % data['email']}), 401

    user = User(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize())


api.add_resource(UserListApi, '/api/users/')
api.add_resource(UserApi, '/api/users/<user_id>/')

# debug in file if DEBUG is False
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(INFO)
    file_handler.setLevel(INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# start app
if __name__ == '__main__':
    app.run()
