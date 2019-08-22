from flask import Blueprint, request, make_response
from flask_restplus import Api, Resource, fields

from project.util.response import m_response
from werkzeug.datastructures import FileStorage
from flask import current_app as app
from werkzeug.utils import secure_filename

from flask_jwt_extended import jwt_required, get_jwt_identity

from pathlib import Path
from project.util.config import conf
from project.util.file_control import email_normalize, delete, save, create_photo_info
from project.database.model_ddb import User, photo_deserialize
from project.solution import solution_put_photo_info_ddb, solution_delete_photo_from_ddb
import os, uuid

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


@api.route('/ping')
@api.doc('photos ping!')
class Ping(Resource):
    @api.doc(responses={200: 'pong success'})
    @jwt_required
    def get(self):
        app.logger.debug('success:pong!')
        return m_response(True, {'msg': 'pong!'}, 200)


@api.route('/file')
@api.expect(file_upload_parser)
class FileUpload(Resource):
    @jwt_required
    def post(self):
        try:
            app.logger.debug(dir(file_upload_parser))
            form = file_upload_parser.parse_args()
            filename_orig = form['file'].filename
            extension = (filename_orig.rsplit('.', 1)[1]).lower()

            if extension.lower() not in ['jpg', 'jpeg', 'bmp', 'gif', 'png']:
                app.logger.error('ERROR:file format is not supported:{0}'.format(filename_orig))
                return m_response(False, {'filename': filename_orig,
                                          'msg': 'not supported file format:{}'.format(extension)}, 400)

            current_user = get_jwt_identity()

            filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
            filesize = save(form['file'], filename, current_user['email'])
            user_id = current_user['user_id']

            new_photo = create_photo_info(filename, filesize, form)
            # TODO 3: Implement following solution code to update photo information into User table
            solution_put_photo_info_ddb(user_id, new_photo)

            return make_response({'ok': True, "photo_id": filename}, 200)
        except Exception as e:
            app.logger.error('ERROR:file upload failed:user_id:{}'.format(get_jwt_identity()['user_id']))
            app.logger.error(e)
            return make_response({'ok': False, 'data': {'user_id': get_jwt_identity()['user_id']}}, 500)




@api.route('/')
class List(Resource):
    @api.doc(
        responses=
        {
            200: "Return the whole photos list",
            500: "Internal server error"
        }
    )
    @jwt_required
    def get(self):
        """Get all photos as list"""
        try:
            user = get_jwt_identity()
            photos = User.get(user['user_id']).photos

            data = {
                'photos': []
            }

            for photo in photos:
                data['photos'].append(photo_deserialize(photo))

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
    @jwt_required
    def delete(self, photo_id):
        """one photo delete"""
        try:
            user = get_jwt_identity()
            photos = User.get(user['user_id']).photos

            for photo in photos:
                if photo.id != photo_id:
                    continue

                filename = photo.filename
                file_deleted = delete(filename, user['email'])

                # TODO 4: Implement following solution code to delete a photo from Photos which is a list
                solution_delete_photo_from_ddb(user, photos, photo)

                if file_deleted:
                    app.logger.debug("success:photo deleted: photo_id:{}".format(photo_id))
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
    @jwt_required
    @api.expect(photo_get_parser)
    def get(self, photo_id):
        """
        Return image for thumbnail and original photo.
        :param photo_id: target photo id
        :queryparam mode: None(original) or thumbnail
        :return: image url for authenticated user
        """
        try:
            mode = request.args.get('mode')
            user = get_jwt_identity()
            email = user['email']
            path = os.path.join(conf['UPLOAD_DIR'], email_normalize(email))
            full_path = Path(path)

            photos = User.get(user['user_id']).photos

            for photo in photos:
                if photo.id == photo_id:
                    if mode == "thumbnail":
                        full_path = full_path / "thumbnails" / photo.filename
                    else:
                        full_path = full_path / photo.filename

            with full_path.open('rb') as f:
                contents = f.read()
                resp = make_response(contents)

            app.logger.debug("filepath:{}".format(str(full_path)))
            resp.content_type = "image/jpeg"
            return resp
        except Exception as e:
            app.logger.error('ERROR:get photo failed:photo_id:{}'.format(photo_id))
            app.logger.error(e)
            return 'http://placehold.it/400x300'

