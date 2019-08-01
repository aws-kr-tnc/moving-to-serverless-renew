
from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Resource, Api, fields
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful_swagger import swagger

from sqlalchemy import exc
from project import db
from project.api.models import User
from project import login
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
import re

users_blueprint = Blueprint('users', __name__)
api = swagger.docs(Api(users_blueprint), apiVersion='0.1')


@swagger.model
class New_user:
    def __init__(self, email, username, password):
        resource_fields = {
            'email': fields.String,
            'username':fields.String,
            'password':fields.String
        }


@swagger.model
class Signin_user:
    def __init__(self, email, password):
        resource_fields = {
            'email': fields.String,
            'password':fields.String
        }

@swagger.model
class Response:
    def __init__(self, message, code):
        pass

class UsersPing(Resource):
    @swagger.operation(
        notes='test ping, answers pong!',
        nickname='PING',
        responseClass=Response.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Always Success"
            }
          ]
        )
    def get(self):
        return response_with_msg(200, 'pong!')

class UsersList(Resource):
    @swagger.operation(
        notes='get the whole users list',
        responseClass=Response.__name__,
        responseMessages=[
            {
                "code":200,
                "message":"Return the whole users list"

            },
            {
                "code": 500,
                "message": "Internal server error"
            }
        ]
    )
    def get(self):
        """Get all users"""
        msg = {
            'users': [user.to_json() for user in User.query.all()]
        }
        return response_with_msg(200, msg)

class Users(Resource):
    @swagger.operation(
        notes='get one user data',
        responseClass=Response.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "Return a user data"

            },
            {
                "code": 500,
                "message": "Internal server error"
            }
        ]
    )
    def get(self, user_id):
        """Get single user details"""

        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if user is None:
                return response_with_msg_data(404, "Not exist user id", {"user": {"id": user_id}})

            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }
            return response_with_data(200, data)
        except ValueError:
            return default_response(400)

class Signup(Resource):
    @swagger.operation(
        notes='register a user',
        responseClass=Response.__name__,
        parameters=[
            {
                "name": "body",
                "description": "necessary email, username, password with json",
                "required": True,
                "allowMultiple": False,
                "dataType": New_user.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Return a user data"

            },
            {
                "code": 400,
                "message": "Invalidate email/password"
            },
            {
                "code": 500,
                "message": "Internal server error"
            }
        ]
    )
    def post(self):
        post_data = request.get_json()

        if not post_data:
            return default_response(400)

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')

        if None in (username, email, password):
            return default_response(400)

        if not data_validate(email, password):
            return response_with_msg(400, 'email or password not valid')

        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email, password=generate_password_hash(password)))
                db.session.commit()
                committed_user = User.query.filter_by(email=email).first()

                data= {
                    "user": {
                    "email": committed_user.email,
                    "username": committed_user.username,
                    "id": committed_user.id
                    }
                }

                return response_with_msg_data(201, "Signup Success!", data)

            return response_with_msg(400, 'Sorry. This email already exists.')
        except ValueError:
            db.session.rollback()
            return response_with_msg(500, 'Undefined status code.')
        except exc.IntegrityError:
            db.session.rollback()
            return default_response(500)

class Signin(Resource):
    @swagger.operation(
        notes='register a user',
        responseClass=Response.__name__,
        parameters=[
            {
                "name": "body",
                "description": "necessary email, password with json",
                "required": True,
                "allowMultiple": False,
                "dataType": Signin_user.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "login success"

            },
            {
                "code": 400,
                "message": "Invalidate data"
            },
            {
                "code": 500,
                "message": "Internal server error"
            }
        ]
    )
    def post(self):
        post_data = request.get_json()

        if not post_data:
            return default_response(400)

        email = post_data.get('email')
        password = post_data.get('password')

        if not data_validate(email, password):
            return response_with_msg(400, 'email or password not valid')

        db_user = db.session.query(User).filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):
            app.logger.debug("login success: id: %s | email: %s" % (db_user.id, db_user.email))
            login_user(db_user)
            return response_with_msg(200, "Login Success!")
        else:
            app.logger.debug('user login failed: %s' % db_user)
            return response_with_msg(400, "Login Failed")

class Signout(Resource):
    @swagger.operation(
        notes='Signout',
        responseClass=Response.__name__,
        responseMessages=[
            {
                "code": 200,
                "message": "signout success"

            }
        ]
    )
    def post(self):
        app.logger.debug('Sign-out : %s', current_user.username)
        logout_user()
        return response_with_msg(200, "Signout success!")


@login.user_loader
def user_loader(user_id):
    result = User.query.get(user_id)
    if not result:
        return None
    return result

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