from flask import Blueprint, request, make_response
from flask_restplus import Api, Resource, fields

from project.util.blacklist_helper import token_decoder, pyjwt_required, get_cognito_user
from project.util.response import m_response
from werkzeug.datastructures import FileStorage
from flask import current_app as app
from werkzeug.utils import secure_filename

from project.util.file_control import delete_s3, save_s3, create_photo_info, presigned_url
from project.db.model_ddb import User
from project.solution.solution import solution_put_photo_info_ddb, solution_delete_photo_from_ddb
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
    'taken_date': fields.DateTime("%Y:%m:%d %H:%M:%S"),
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

def get_token_from_header(request):
    return request.headers['Authorization'].rsplit(' ', 1)[1]


@api.route('/ping')
@api.doc('photos ping!')
class Ping(Resource):
    @api.doc(responses={200: 'pong success'})
    @pyjwt_required
    def get(self):

        app.logger.debug('success:pong!')
        return m_response(True, {'msg': 'pong!'}, 200)


@api.route('/file')
@api.expect(file_upload_parser)
class FileUpload(Resource):
    @pyjwt_required
    def post(self):
        token = get_token_from_header(request)
        try:
            app.logger.debug(dir(file_upload_parser))
            form = file_upload_parser.parse_args()
            filename_orig = form['file'].filename
            extension = (filename_orig.rsplit('.', 1)[1]).lower()

            if extension.lower() not in ['jpg', 'jpeg', 'bmp', 'gif', 'png']:
                app.logger.error('ERROR:file format is not supported:{0}'.format(filename_orig))
                return m_response(False, {'filename': filename_orig,
                                          'msg': 'not supported file format:{}'.format(extension)}, 400)

            current_user = get_cognito_user(token)

            filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))

            filesize = save_s3(form['file'], filename, current_user['email'])
            user_id = current_user['user_id']

            new_photo = create_photo_info(filename, filesize, form)

            solution_put_photo_info_ddb(user_id, new_photo)

            return make_response({'ok': True, "photo_id": filename}, 200)
        except Exception as e:
            app.logger.error('ERROR:file upload failed:user_id:{}'.format(get_cognito_user(token)['user_id']))
            app.logger.error(e)
            return make_response({'ok': False, 'data': {'user_id': get_cognito_user(token)['user_id']}}, 500)




@api.route('/')
class List(Resource):
    @api.doc(
        responses=
        {
            200: "Return the whole photos list",
            500: "Internal server error"
        }
    )
    @pyjwt_required
    def get(self):
        """Get all photos as list"""
        token = get_token_from_header(request)
        try:
            user = get_cognito_user(token)
            photos = User.get(user['user_id']).photos

            data = {
                'photos': []
            }

            for photo in photos:
                url = presigned_url(photo.id, user['email'], False)
                data['photos'].append(url)

            app.logger.debug("success:photos_list:%s" % data)
            return m_response(True, data, 200)

        except Exception as e:
            app.logger.error("ERROR:photos list failed")
            app.logger.error(e)
            return m_response(False, None, 500)


@api.route('/<photo_id>')
class OnePhoto(Resource):
    @api.doc(
        responses=
        {
            200: "Delete success",
            404: "file not exist",
            500: "Internal server error"
        }
    )
    @pyjwt_required
    def delete(self, photo_id):
        """one photo delete"""
        token = get_token_from_header(request)
        try:
            user = get_cognito_user(token)
            photos = User.get(user['user_id']).photos

            for photo in photos:
                if photo.id != photo_id:
                    continue

                filename = photo.filename
                file_deleted = delete_s3(filename, user['email'])


                solution_delete_photo_from_ddb(user, photos, photo)

                if file_deleted:
                    app.logger.debug("success:photo deleted: user_id:{}, photo_id:{}".format(user['user_id'], photo_id))
                    return m_response(True, {'photo_id': photo_id}, 200)
                else:
                    raise FileNotFoundError

        except FileNotFoundError as e:
            app.logger.error('ERROR:not exist photo_id:{}'.format(photo_id))
            return m_response(False, {'photo_id': photo_id}, 404)
        except Exception as e:
            app.logger.error("ERROR:photo delete failed: photo_id:{}".format(photo_id))
            app.logger.error(e)
            return m_response(False, {'photo_id': photo_id}, 500)

    @api.doc(
        responses=
        {
            200: "Success",
            500: "Internal server error"
        }
    )
    @pyjwt_required
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