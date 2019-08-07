
from flask import Blueprint, request
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import exc
from project import db
from project.api.models import User
from project import login
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
from flask_restplus import Api, Resource, fields

import re
from project.schemas import validate_user
from flask_jwt_extended import (create_access_token, create_refresh_token, JWTManager,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask import jsonify, make_response

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint, doc='/swagger/', title='Users',
          description='CloudAlbum-users: \n prefix url "/users" is already exist.', version='0.1')

response = api.model('Response', {
    'code': fields.Integer,
    'message':fields.String,
    'data':fields.String
})

signup_user = api.model ('Signup_user',{
    'email': fields.String,
    'username':fields.String,
    'password':fields.String
})

signin_user = api.model ('Signin_user',{
    'email': fields.String,
    'password':fields.String
})


@api.route('/ping')
class UsersPing(Resource):
    @api.marshal_with(response)
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug("ping success!")
        return response_with_msg(200, 'pong!')


@api.route('/')
class UsersList(Resource):
    @api.doc(
        responses=
            {
                200:"Return the whole users list",
                500: "Internal server error"
            }
        )
    @api.marshal_with(response)
    def get(self):
        """Get all users as list"""
        try:
            users = [user.to_json() for user in User.query.all()]
            data = {
                'users': users
            }
            app.logger.debug("success:users_list:%s" % users)

            return response_with_data(200, data)
        except:
            app.logger.debug("users list failed:users list:%s" % users)
            return default_response(500)


@api.route('/<user_id>')
class Users(Resource):
    @api.doc(responses={
                200: "Return a user data",
                500: "Internal server error"
            })
    @api.marshal_with(response)
    def get(self, user_id):
        """Get a single user details"""
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
            app.logger.debug("success:user_get_by_id:%s" % data['user'])
            return response_with_data(200, data)
        except ValueError:
            app.logger.debug("ERROR:user_get_by_id:%s" % data['user'])
            return default_response(400)


@api.route('/signup')
class Signup(Resource):
    @api.doc(responses={
        201: "Return a user data",
        400: "Invalidate email/password",
        500: "Internal server error"
    })
    @api.expect(signup_user)
    @api.marshal_with(response)
    def post(self):
        """Enroll a new user"""
        post_data = validate_user(request.get_json())

        if post_data['ok']:
            data = post_data['data']
            try:
                user = User.query.filter_by(email=data['email']).first()
                if not user:
                    db.session.add(User(username=data['username'],
                                        email=data['email'],
                                        password=generate_password_hash(data['password'])))
                    db.session.commit()
                    app.logger.debug('success:user_signup: {0}'.format(data['data']))
                    return response_with_msg_data(201, "Signup Success!", data['data'])
            except:
                return default_response(500)

        else:
            app.logger.debug('ERROR:user_signup:invalidation failed: {0}'.format(post_data))
            return response_with_msg_data(400, post_data['message'], post_data)


@api.route('/signin')
class Signin(Resource):
    @api.doc(responses={
        200:'login success',
        400: 'Invalidate data',
        500: 'Internal server error'
    })
    @api.expect(signin_user)
    # @api.marshal_with(response)
    def post(self):
        """user signin"""
        try:
            post_data = validate_user(request.get_json())
            if post_data['ok']:
                data = post_data['data']
                user = db.session.query(User).filter_by(email=data['email']).first()
                user = user.to_json()

                if user and check_password_hash(user['password'], data['password']):
                    del user['password']
                    access_token = create_access_token(identity=data)
                    refresh_token = create_refresh_token(identity=data)
                    user['token'] = access_token
                    user['refresh'] = refresh_token
                    return make_response(jsonify({'ok': True, 'data': user}), 200)

                else:
                    app.logger.debug('ERROR:user signin failed:password unmatched: {0}'.format(data['email']))
                    return response_with_msg(400, "Login Failed")

        except Exception as e:
            app.logger.debug('ERROR: {0}'.format(e))
            app.logger.debug('ERROR:user signin failed:unknown issue:{0}'.format(data['email']))
            return default_response(500)


@api.route('/signout')
class Signout(Resource):
    @login_required
    @api.doc(responses={
        200:'signout success',
        500:'login required'
    })
    @api.marshal_with(response)
    def post(self):
        """user signout"""
        try:
            username = current_user.username
            logout_user()
            app.logger.debug('success:Sign-out:%s', username)
            return response_with_msg(200, "Signout success!")
        except:
            app.logger.debug('ERROR:Sign-out:unknown issue:%s', username)
            return default_response(500)


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
