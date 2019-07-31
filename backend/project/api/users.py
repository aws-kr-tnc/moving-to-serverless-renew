
from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Resource, Api
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import exc
from project import db
from project.api.models import User
from project import login
import re

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)


class UsersPing(Resource):
    def get(self):
        return response_util(200, 'pong!')

class UsersList(Resource):
    def get(self):
        """Get all users"""
        msg = {
            'data': {
                'users': [user.to_json() for user in User.query.all()]
            }
        }
        return response_util(200, msg)

class Users(Resource):
    def get(self, user_id):
        """Get single user details"""

        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if user is None:
                return response_util(404)
            else:
                msg = {
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }
                return response_util(200, msg)
        except ValueError:
            return response_util(404)

class Signup(Resource):
    def post(self):
        post_data = request.get_json()

        if not post_data:
            return response_util(400)

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')

        if None in (username, email, password):
            return response_util(400)

        if not data_validate(email, password):
            return response_util(400, 'email or password not valid')

        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email, password=generate_password_hash(password)))
                db.session.commit()
                return response_util(201, '%s was added!' % email)
            else:
                return response_util(400, 'Sorry. This email already exists.')
        except ValueError:
            db.session.rollback()
            return response_util(500, 'Undefined status code.')
        except exc.IntegrityError:
            db.session.rollback()
            return response_util(500)

class Signin(Resource):
    def post(self):
        post_data = request.get_json()

        if not post_data:
            return response_util(400)

        email = post_data.get('email')
        password = post_data.get('password')

        if not data_validate(email, password):
            return response_util(400, 'email or password not valid')

        db_user = db.session.query(User).filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):
            app.logger.debug("login success: id: %s | email: %s" % (db_user.id, db_user.email))
            login_user(db_user)
            return response_util(200)
        else:
            app.logger.debug('user login failed: %s' % db_user)
            return response_util(400, "Login Failed")


class Signout(Resource):
    def post(self):
        app.logger.debug('Sign-out : %s', current_user.username)
        logout_user()
        return response_util(200)

@login.user_loader
def user_loader(user_id):
    result = User.query.get(user_id)
    if not result:
        return None
    return result

dic_response = {200 : { 'status': 200,
                         'message': 'Success'},
                201 : { 'status': 201,
                         'message': 'Created'},
                400 : { 'status': 400,
                         'message': 'Invalid payload'},
                404 : { 'status': 404,
                         'message':'User not exist'},
                500 : { 'status': 500,
                         'message': 'Internal server error'}
                 }

def response_util(response_code):
    try:
        if response_code in dic_response:
            return dic_response[response_code], response_code
        else:
            raise ValueError
    except:
        raise ValueError

def response_util(response_code, msg):
    try:
        if response_code in dic_response:
            res = dic_response[response_code]
            res['message'] = msg
            return res, response_code
        else:
            raise ValueError
    except:
        app.logger.debug("Undefined error: %s" % response_code)
        raise ValueError


def data_validate(email, password):
    email_regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    if not re.match(email_regex, email) or (len(password) <= 1):
        return False
    return True


api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')
api.add_resource(Signup, '/users/signup')
api.add_resource(Signin, '/users/signin')
api.add_resource(Signout, '/users/signout')