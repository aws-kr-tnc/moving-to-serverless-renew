"""
    cloudalbum/api/photos.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    REST API for photos

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint, request, make_response
from flask import current_app as app
from flask_restplus import Api, Resource, fields
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, InternalServerError
from cloudalbum.database.model_ddb import Photo
from cloudalbum.solution import solution_put_photo_info_ddb
from cloudalbum.util.file_control import delete_s3, save_s3, with_presigned_url, presigned_url
from cloudalbum.util.jwt_helper import cog_jwt_required, get_token_from_header, get_cognito_user
import uuid


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

photos_blueprint = Blueprint('photos', __name__)
api = Api(photos_blueprint, doc='/swagger/',
          title='Photos',
          description='CloudAlbum-photos: \n prefix url "/photos" is already exist.\n '
                      'Due to JWT token is required, to test this api, please follow under instruction.\n'
                      '1. Get  your access token which you can get /users/signin with registered user email. \n'
                      '2. Copy your access token, and click Authorize button which located in right bottom of this description \n'
                      '3. Input your access token with this format: "Bearer <copied jwt token>", into value box.'
                      '4. click Authorize, and close the popup. now you can start your test.',
          version='0.1',
          security='Bearer Auth',
          authorizations=authorizations)

photo_info = api.model('New_photo', {
    'tags': fields.String,
    'desc': fields.String,
    'geotag_lat': fields.Float,
    'geotag_lng': fields.Float,
    'taken_date': fields.DateTime('%Y:%m:%d %H:%M:%S'),
    'make': fields.String,
    'model': fields.String,
    'width': fields.String,
    'height': fields.String,
    'city': fields.String,
    'nation': fields.String,
    'address': fields.String
})

photo_get_parser = api.parser()
photo_get_parser.add_argument('mode', type=str, location='args')

file_upload_parser = api.parser()
file_upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
file_upload_parser.add_argument('tags', type=str, location='form')
file_upload_parser.add_argument('desc', type=str, location='form')
file_upload_parser.add_argument('make', type=str, location='form')
file_upload_parser.add_argument('model', type=str, location='form')
file_upload_parser.add_argument('width', type=str, location='form')
file_upload_parser.add_argument('height', type=str, location='form')
file_upload_parser.add_argument('taken_date', type=str, location='form')
file_upload_parser.add_argument('geotag_lat', type=str, location='form')
file_upload_parser.add_argument('geotag_lng', type=str, location='form')
file_upload_parser.add_argument('city', type=str, location='form')
file_upload_parser.add_argument('address', type=str, location='form')
file_upload_parser.add_argument('nation', type=str, location='form')


@api.route('/ping')
@api.doc('photos ping!')
class Ping(Resource):
    @api.doc(responses={200: 'pong success'})
    @cog_jwt_required
    def get(self):
        app.logger.debug('success:pong!')
        return make_response({'ok': True, 'Message': 'pong'}, 200)


@api.route('/file')
@api.expect(file_upload_parser)
class FileUpload(Resource):
    @cog_jwt_required
    def post(self):
        form = file_upload_parser.parse_args()
        filename_orig = form['file'].filename
        token = get_token_from_header(request)
        extension = (filename_orig.rsplit('.', 1)[1]).lower()
        current_user = get_cognito_user(token)

        if extension.lower() not in ['jpg', 'jpeg', 'bmp', 'gif', 'png']:
            app.logger.error('File format is not supported:{0}'.format(filename_orig))
            raise BadRequest('File format is not supported:{0}'.format(filename_orig))

        try:
            filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
            filesize = save_s3(form['file'], filename, current_user['email'])
            user_id = current_user['user_id']

            solution_put_photo_info_ddb(user_id, filename, form, filesize)
            return make_response({'ok': True}, 200)
        except Exception as e:
            app.logger.error('ERROR:file upload failed:user_id:{}'.format(current_user['user_id']))
            app.logger.error(e)
            raise InternalServerError('File upload failed: {0}'.format(e))


@api.route('/')
class List(Resource):
    @api.doc(
        responses=
        {
            200: 'Return the whole photos list',
            500: 'Internal server error'
        }
    )
    @cog_jwt_required
    def get(self):
        """Get all photos as list"""
        token = get_token_from_header(request)
        try:
            user = get_cognito_user(token)
            photos = Photo.query(user['user_id'])
            data = {'photos': []}
            [data['photos'].append(with_presigned_url(user, photo)) for photo in photos]
            app.logger.debug('success:photos_list: {}'.format(data))
            return make_response({'ok': True, 'photos': data['photos']}, 200)

        except Exception as e:
            app.logger.error('ERROR:photos list failed')
            app.logger.error(e)
            raise InternalServerError('Photos list retrieving failed')


@api.route('/<photo_id>')
class OnePhoto(Resource):
    @api.doc(
        responses=
        {
            200: 'Delete success',
            404: 'file not exist',
            500: 'Internal server error'
        }
    )
    @cog_jwt_required
    def delete(self, photo_id):
        """one photo delete"""
        token = get_token_from_header(request)
        user = get_cognito_user(token)
        try:
            photo = Photo.get(user['user_id'], photo_id)
            photo.delete()
            file_deleted = delete_s3(photo.filename, user['email'])

            if file_deleted:
                app.logger.debug("success:photo deleted: user_id:{}, photo_id:{}".format(user['user_id'], photo_id))
                return make_response({'ok': True, 'photos': {'photo_id': photo_id}}, 200)
            else:
                raise FileNotFoundError
        except FileNotFoundError as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

    @api.doc(
        responses=
        {
            200: 'Success',
            500: 'Internal server error'
        }
    )
    @cog_jwt_required
    @api.expect(photo_get_parser)
    def get(self, photo_id):
        token = get_token_from_header(request)
        try:
            mode = request.args.get('mode')
            user = get_cognito_user(token)
            email = user['email']
            return presigned_url(photo_id, email, True if mode else False)
        except Exception as e:
            app.logger.error('ERROR:get photo failed:photo_id:{}'.format(photo_id))
            app.logger.error(e)
            return 'http://placehold.it/400x300'
