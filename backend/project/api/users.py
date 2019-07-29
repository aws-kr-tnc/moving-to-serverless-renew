
from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc
from project import db
from project.api.models import User

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

def util_create_response(status, msg):
    return {
        'status': status,
        'message': msg
    }

class UsersPing(Resource):
    def get(self):
        return util_create_response('success', 'pong!')


class UsersList(Resource):

    def post(self):
        post_data = request.get_json()

        if not post_data:
            return util_create_response('fail', 'Invalid payload'), 400

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')

        if None in (username, email, password):
            return util_create_response('fail', 'Invalid payload'), 400

        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email, password=password))
                db.session.commit()
                return util_create_response('success', '%s was added!' % email), 201
            else:
                return util_create_response('fail', 'Sorry. That email already exists.'), 400

        except exc.IntegrityError:
            db.session.rollback()
            return util_create_response('fail', 'Invalid payload'), 400

    def get(self):
        """Get all users"""
        msg = {
            'data': {
                'users': [user.to_json() for user in User.query.all()]
            }
        }
        return util_create_response('success', msg), 200


class Users(Resource):
    def get(self, user_id):
        """Get single user details"""

        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return util_create_response('fail', 'User does not exist'), 404
            else:
                msg = {
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }
                return util_create_response('success', msg), 200
        except ValueError:
            return util_create_response('fail', 'User does not exist'), 404


api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')

