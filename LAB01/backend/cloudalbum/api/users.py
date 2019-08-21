
from flask import Blueprint, request
from flask import current_app as app
from jsonschema import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from cloudalbum import db, jwt
from cloudalbum.api.models import User
from flask_restplus import Api, Resource, fields

from cloudalbum.schemas import validate_user
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify, make_response
from cloudalbum.util.response import m_response
from cloudalbum.util.blacklist_helper import add_token_to_database

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
class Ping(Resource):
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug("success:ping pong!")
        return m_response(True, {'msg':'pong!'}, 200)

@api.route('/')
class UsersList(Resource):
    @api.doc(
        responses=
            {
                200:"Return the whole users list",
                500: "Internal server error"
            }
        )
    def get(self):
        """Get all users as list"""
        try:
            users = [user.to_json() for user in User.query.all()]
            data = {
                'users': users
            }

            app.logger.debug("success:users_list:%s" % users)
            return m_response(True, data, 200)

        except Exception as e:
            app.logger.error("users list failed:users list:%s" % data)
            app.logger.error(e)
            return make_response(False, data, 500)


@api.route('/<user_id>')
class Users(Resource):
    @api.doc(responses={
                200: "Return a user data",
                500: "Internal server error"
            })
    def get(self, user_id):
        """Get a single user details"""
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if user is None:
                app.logger.error('ERROR:user_id not exist:{}'.format(user_id))
                return m_response(False, {'user_id': user_id}, 404)

            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }
            app.logger.debug("success:user_get_by_id:%s" % data['user'])
            return m_response(True, data, 200)
        except ValueError as e:
            app.logger.error("ERROR:user_get_by_id:{}".format(user_id))
            app.logger.error(e)
            return m_response(False, {'user_id':user_id}, 500)
        except Exception as e:
            app.logger.error("ERROR:user_get_by_id:{}".format(user_id))
            app.logger.error(e)
            return m_response(False, {'user_id': user_id}, 500)


@api.route('/signup')
class Signup(Resource):
    @api.doc(responses={
        201: "Return a user data",
        400: "Invalidate email/password",
        500: "Internal server error"
    })
    @api.expect(signup_user)
    def post(self):
        """Enroll a new user"""
        req_data = request.get_json()
        try:
            validated = validate_user(req_data)
            user_data = validated['data']
            db_user = User.query.filter_by(email=user_data['email']).first()
            email = user_data['email']
            if not db_user:
                db.session.add(User(username=user_data['username'],
                                    email=email,
                                    password=generate_password_hash(user_data['password'])))
                db.session.commit()

                committed_user = User.query.filter_by(email=email).first()

                user = {
                    "id": committed_user.id,
                    'username': committed_user.username,
                    'email': committed_user.email

                }
                app.logger.debug('success:user_signup: {0}'.format(user))
                return m_response(True, user, 201)
            else:
                app.logger.error('ERROR:exist user: {0}'.format(user_data))
                return m_response(False, user_data, 409)
        except ValidationError as e:
            app.logger.error('ERROR:invalid signup data format:{0}'.format(req_data))
            app.logger.error(e)
            return m_response(False, req_data,400)
        except Exception as e:
            app.logger.error('ERROR:unexpected signup error:{}'.format(req_data))
            app.logger.error(e)
            return m_response(False, req_data, 500)


@api.route('/signin')
class Signin(Resource):
    @api.doc(responses={
        200: 'login success',
        400: 'Invalidate data',
        500: 'Internal server error'
    })
    @api.expect(signin_user)
    def post(self):
        """user signin"""
        req_data = request.get_json()
        try:
            signin_data = validate_user(req_data)['data']

            db_user = db.session.query(User).filter_by(email=signin_data['email']).first()
            if db_user is None:
                return m_response(False, {'msg':'not exist email', 'user':signin_data}, 400)

            token_data = {'user_id': db_user.id, 'username':db_user.username, 'email':db_user.email}

            if db_user is not None and check_password_hash(db_user.password, signin_data['password']):

                access_token = create_access_token(identity=token_data)
                refresh_token = create_refresh_token(identity=token_data)
                res = jsonify({'accessToken': access_token, 'refreshToken': refresh_token})
                app.logger.debug('success:user signin:{}'.format(token_data))
                return make_response(res, 200)
            else:
                app.logger.error('ERROR:user signin failed:password unmatched or invalid user: {0}'.format(signin_data))
                return m_response(False, {'msg':'password unmatched or invalid user',
                                          'user': signin_data}, 400)

        except ValidationError as e:
            app.logger.error('ERROR:invalid data format:{0}'.format(req_data))
            app.logger.error(e)
            return m_response(False, {'msg':e.message, 'user':req_data} ,400)
        except Exception as e:
            app.logger.error('ERROR:unexpected error:{0}'.format(req_data))
            app.logger.error(e)
            return m_response(False, req_data, 500)


@api.route('/signout', doc=False)
class Signout(Resource):
    @jwt_required
    @api.doc(responses={
        200:'signout success',
        500:'login required'
    })
    def post(self):
        """user signout"""
        try:
            # TODO: jwt token stored in DB version
            user = get_jwt_identity()
            add_token_to_database(get_raw_jwt())
            return m_response(True, {'user':user, 'msg':'logged out'}, 200)

            # TODO: jwt token stored in memory version
            # add_token_to_set(get_raw_jwt())
            # return m_response(True, {'user': user, 'msg': 'logged out'}, 200)

        except Exception as e:
            app.logger.error('ERROR:Sign-out:unknown issue:user:{}'.format(get_jwt_identity()))
            app.logger.error(e)
            return m_response(False, get_jwt_identity(), 500)

