import hashlib
import uuid

import boto3, hmac, base64

from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify, make_response
from flask_restplus import Api, Resource, fields

from jsonschema import ValidationError


from project.schemas import validate_user
from project.db.model_ddb import User
from project.solution.solution import solution_put_new_user, solution_get_user_data_with_idx
from project.util.response import m_response
from project.util.blacklist_helper import add_token_to_set
from project.util.config import conf

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
            data = []

            for user in User.scan():
                one_user = {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username
                }
                data.append(one_user)

            app.logger.debug("success:users_list:%s" % data)
            return m_response(True, data, 200)

        except Exception as e:
            app.logger.error("users list failed")
            app.logger.error(e)
            return m_response(False, None, 500)


@api.route('/<user_id>')
class Users(Resource):
    @api.doc(responses={
                200: "Return a user data",
                500: "Internal server error"
            })
    def get(self, user_id):
        """Get a single user details"""
        try:
            for user in User.query(hash_key=user_id):
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

def cognito_signup(signup_user):
    user = signup_user;
    msg = '{0}{1}'.format(user['email'], conf['COGNITO_CLIENT_ID'])
    client = boto3.client('cognito-idp')
    dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                   msg=msg.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()

    response = client.sign_up(
        ClientId=conf['COGNITO_CLIENT_ID'],
        SecretHash=base64.b64encode(dig).decode(),
        Username=user['email'],
        Password=user['password'],
        UserAttributes=[
            {
                'Name': 'name',
                'Value': user['username']
            }
        ],
        ValidationData=[
            {
                'Name': 'name',
                'Value': user['username']
            }
        ]

    )
    print(response)

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
            cognito_signup(user_data)
            exist_user = None
            email = user_data['email']

            for item in User.email_index.query(email):
                exist_user = item

            if not exist_user:
                new_user_id = uuid.uuid4().hex

            #     solution_put_new_user(new_user_id, user_data)

                user = {
                    "id": new_user_id,
                    'username': user_data['username'],
                    'email': email
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


def cognito_signin(user):
    client = boto3.client('cognito-idp')
    try:
        msg = '{0}{1}'.format(user['email'], conf['COGNITO_CLIENT_ID'])

        dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                       msg=msg.encode('utf-8'),
                       digestmod=hashlib.sha256).digest()
        auth= base64.b64encode(dig).decode()
        resp = client.admin_initiate_auth(UserPoolId=conf['COGNITO_POOL_ID'],
                                          ClientId=conf['COGNITO_CLIENT_ID'],
                                          AuthFlow='ADMIN_NO_SRP_AUTH',
                                          AuthParameters={'SECRET_HASH': auth,'USERNAME': user['email'], 'PASSWORD': user['password']})
        print("secret key:{}".format(auth))
        access_token = resp['AuthenticationResult']['AccessToken']
        refresh_token = resp['AuthenticationResult']['RefreshToken']
        id_token = resp['AuthenticationResult']['IdToken']

        return access_token, refresh_token, id_token
    except client.exceptions.NotAuthorizedException as e:
        app.logger.error("password mismatched")
        app.logger.error(e)
        raise e


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
        client = boto3.client('cognito-idp')
        try:
            signin_data = validate_user(req_data)['data']

            access_token, refresh_token, id_token = cognito_signin(signin_data)
            # print("idtoken:{}".format(id_token))
            res = jsonify({'accessToken': access_token, 'refreshToken': refresh_token})
            app.logger.debug('success:user signin:access_token:{}, refresh_token:{}'.format(access_token, refresh_token))
            return make_response(res, 200)

        except client.exceptions.NotAuthorizedException as e:
            app.logger.error('ERROR:user signin failed:password unmatched or invalid user: {0}'.format(signin_data))
            app.logger.error(e)
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


@api.route('/signout')
class Signout(Resource):
    @jwt_required
    @api.doc(responses={
        200:'signout success',
        500:'login required'
    })
    def post(self):
        """user signout"""
        try:
            user = get_jwt_identity()
            add_token_to_set(get_raw_jwt())

            app.logger.debug("user token signout: {}".format(user))
            return m_response(True, {'user':user, 'msg':'logged out'}, 200)

        except Exception as e:
            app.logger.error('ERROR:Sign-out:unknown issue:user:{}'.format(get_jwt_identity()))
            app.logger.error(e)
            return m_response(False, get_jwt_identity(), 500)

