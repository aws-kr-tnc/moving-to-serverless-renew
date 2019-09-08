from flask import Blueprint, request, make_response
from flask import current_app as app
from flask import jsonify
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_raw_jwt)
from jsonschema import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from cloudalbum import db
from cloudalbum.database.models import User
from cloudalbum.schemas import validate_user
from cloudalbum.util.jwt_helper import add_token_to_set
from werkzeug.exceptions import BadRequest, InternalServerError, Conflict


users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint, doc='/swagger/', title='Users',
          description='CloudAlbum-users: \n prefix url "/users" is already exist.', version='0.1')

response = api.model('Response', {
    'code': fields.Integer,
    'message': fields.String,
    'data': fields.String
})

signup_user = api.model('Signup_user', {
    'email': fields.String,
    'username': fields.String,
    'password': fields.String
})

signin_user = api.model('Signin_user', {
    'email': fields.String,
    'password': fields.String
})


@api.route('/ping')
class Ping(Resource):
    @api.doc(responses={200: 'pong!'})
    def get(self):
        """Ping api"""
        app.logger.debug("success:ping pong!")
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
            users = [user.to_json() for user in User.query.all()]
            app.logger.debug('success:users_list: {0}'.format(users))
            return make_response({'ok': True, 'users': users}, 200)
        except Exception as e:
            app.logger.error('Retrieve user list failed: {0}'.format(e))
            raise InternalServerError('Retrieve user list failed')


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
                app.logger.error('User_id not exist:{0}'.format(user_id))
                raise BadRequest('User not exist')
            app.logger.debug('success:user_get_by_id: {0}'.format(user))
            return make_response({'ok': True, 'users': user.to_json()}, 200)
        except ValueError as e:
            app.logger.error("user_get_by_id:{0}, {1}".format(user_id, e))
            return InternalServerError(e)
        except Exception as e:
            app.logger.error("Unexpected Error: {0}, {1}".format(user_id, e))
            raise InternalServerError('Unexpected Error:{0}'.format(e))


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
                user = User(username=user_data['username'],
                            email=email, password=generate_password_hash(user_data['password']))
                db.session.add(user)
                db.session.commit()
                return make_response({'ok': True, 'users': user.to_json()}, 201)
            else:
                raise Conflict('ERROR: Existed user!')

        except ValidationError as e:
            app.logger.error('ERROR: {0}\n{1}'.format(e.message, req_data))
            raise BadRequest(e.message)


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
                app.logger.error('Not existed user!')
                raise BadRequest('Not existed user!')
            else:
                if check_password_hash(db_user.password, signin_data['password']):
                    token_data = {'user_id': db_user.id, 'username': db_user.username, 'email': db_user.email}
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


@api.route('/signout', doc=False)
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
            return make_response({'ok': True, 'users': user, 'Message': 'logged out'}, 200)
        except Exception as e:
            app.logger.error('Sign-out:unknown issue:user:{0}: {1}'.format(get_jwt_identity(), e))
            raise BadRequest(e)
