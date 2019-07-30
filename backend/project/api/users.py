
from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Resource, Api
from flask_login import current_user, login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import exc
from project import db
from project.api.models import User
from project import login

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)


class UsersPing(Resource):
    def get(self):
        return util_create_response('success', 'pong!')


class UsersList(Resource):
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

class Signup(Resource):
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
                db.session.add(User(username=username, email=email, password=generate_password_hash(password)))
                db.session.commit()
                return util_create_response('success', '%s was added!' % email), 201
            else:
                return util_create_response('fail', 'Sorry. This email already exists.'), 400

        except exc.IntegrityError:
            db.session.rollback()
            return util_create_response('fail', 'Invalid payload'), 400

class Signin(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        validated = data_validate(email, password)

        if not validated:
            return util_create_response('fail', 'Invalid user data'), 400

        db_user = db.session.query(User).filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):
            app.logger.debug("login success: id: %s | email: %s" % (db_user.id, db_user.email))
            login_user(db_user)
            return util_create_response('success', 'Login success'), 200
        else:
            app.logger.debug('user login failed: %s' % db_user)
            return util_create_response('fail', 'Login failed'), 400


class Signout(Resource):
    def post(self):
        app.logger.debug('Sign-out : %s', current_user.username)
        logout_user()
        return util_create_response('success', 'Signout success.')

@login.user_loader
def user_loader(user_id):
    result = User.query.get(user_id)
    if result is not None:
        return result
    return None



def util_create_response(status, msg):
    return {
        'status': status,
        'message': msg
    }


def data_validate(email, password):
    # TODO implement
    return True


api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')
api.add_resource(Signup, '/users/signup')
api.add_resource(Signin, '/users/signin')
api.add_resource(Signout, '/users/signout')