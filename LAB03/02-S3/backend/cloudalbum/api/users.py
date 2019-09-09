"""
    cloudalbum/api/users.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    REST API for users

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import uuid
from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify, make_response
from flask_restplus import Api, Resource, fields
from jsonschema import ValidationError
from pynamodb.exceptions import PynamoDBException
from werkzeug.exceptions import InternalServerError, BadRequest, Conflict
from werkzeug.security import check_password_hash
from cloudalbum.schemas import validate_user
from cloudalbum.database.model_ddb import User
from cloudalbum.solution import solution_put_new_user, solution_get_user_data_with_idx
from cloudalbum.util.jwt_helper import add_token_to_set

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint, doc='/swagger/', title='Users',
          description='CloudAlbum-users: \n prefix url "/users" is already exist.', version='0.1')


response = api.model('Response', {
    'code': fields.Integer,
    'message': fields.String,
    'data': fields.String
})

signup_user = api.model ('Signup_user',{
    'email': fields.String,
    'username': fields.String,
    'password': fields.String
})

signin_user = api.model ('Signin_user',{
    'email': fields.String,
    'password': fields.String
})


@api.route('/ping')
class Ping(Resource):
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug('success:ping pong!')
        return make_response({'ok': True, 'Message': 'pong'}, 200)


@api.route('/')
class UsersList(Resource):
    @api.doc(
        responses=
            {
                200: 'Return the whole users list',
                500: 'Internal server error'
            }
        )
    def get(self):
        """Get all users as list"""
        try:
            data = []
            for user in User.scan():
                one_user = {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
                data.append(one_user)

            app.logger.debug("success:users_list:%s" % data)
            return make_response({'ok': True, 'users': data}, 200)

        except Exception as e:
            app.logger.error("users list failed")
            app.logger.error(e)
            raise InternalServerError('Retrieve user list failed')


@api.route('/<user_id>')
class Users(Resource):
    @api.doc(responses={
                200: 'Return a user data',
                500: 'Internal server error'
            })
    def get(self, user_id):
        """Get a single user details"""
        try:
            user = [user for user in User.query(hash_key=user_id)]
            if not user:
                app.logger.error('ERROR:user_id not exist:{}'.format(user_id))
                raise BadRequest('User not exist')

            user = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            app.logger.debug('success:user_get_by_id: {0}'.format(user))
            return make_response({'ok': True, 'users': user}, 200)

        except ValueError as e:
            app.logger.error('user_get_by_id:{0}, {1}'.format(user_id, e))
            raise InternalServerError(e)
        except Exception as e:
            app.logger.error('Unexpected Error: {0}, {1}'.format(user_id, e))
            raise InternalServerError('Unexpected Error:{0}'.format(e))


@api.route('/signup')
class Signup(Resource):
    @api.doc(responses={
        201: 'Return a user data',
        400: 'Invalidate email/password',
        500: 'Internal server error'
    })
    @api.expect(signup_user)
    def post(self):
        """Enroll a new user"""
        req_data = request.get_json()
        validated = validate_user(req_data)
        user_data = validated['data']
        try:
            exist_user = [item for item in User.email_index.query(user_data['email'])]
            if not exist_user:
                new_user_id = uuid.uuid4().hex
                solution_put_new_user(new_user_id, user_data)

                user = {
                    'id': new_user_id,
                    'username': user_data['username'],
                    'email': user_data['email']
                }

                app.logger.debug('success:user_signup: {0}'.format(user))
                return make_response({'ok': True, 'users': user}, 201)
            else:
                app.logger.error('ERROR: Existed user: {0}'.format(user_data))
                raise Conflict('ERROR: Existed user!')
        except ValidationError as e:
            app.logger.error('ERROR: {0}\n{1}'.format(e.message, req_data))
            raise BadRequest(e.message)
        except PynamoDBException as e:
            app.logger.error('ERROR: {0}\n{1}'.format(e.msg, req_data))
            raise InternalServerError(e.msg)


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
            db_user = solution_get_user_data_with_idx(signin_data)
            if db_user is None:
                raise BadRequest('Not existed user!')
            else:
                if check_password_hash(db_user.password, signin_data['password']):
                    token_data = {'user_id': db_user.id, 'username':db_user.username, 'email':db_user.email}
                    access_token = create_access_token(identity=token_data)
                    refresh_token = create_refresh_token(identity=token_data)
                    res = jsonify({'accessToken': access_token, 'refreshToken': refresh_token})
                    app.logger.debug('success:user signin:{}'.format(token_data))
                    return make_response(res, 200)
                else:
                    app.logger.error('Password is mismatched or invalid user: {0}'.format(signin_data))
                    raise BadRequest('Password is mismatched or invalid user')

        except ValidationError as e:
            app.logger.error('ERROR: {0}\n{1}'.format(e.message, req_data))
            raise BadRequest(e.message)
        except PynamoDBException as e:
            app.logger.error('ERROR: {0}\n{1}'.format(e.msg, req_data))
            raise InternalServerError(e.msg)


@api.route('/signout')
class Signout(Resource):
    @jwt_required
    @api.doc(responses={
        200: 'signout success',
        500: 'login required'
    })
    def post(self):
        """user signout"""
        try:
            user = get_jwt_identity()
            add_token_to_set(get_raw_jwt())
            app.logger.debug("user token signout: {}".format(user))
            return make_response({'ok': True, 'users': user, 'Message': 'logged out'}, 200)

        except Exception as e:
            app.logger.error('ERROR:Sign-out:unknown issue:user:{}'.format(get_jwt_identity()))
            app.logger.error(e)
            raise BadRequest(e)

