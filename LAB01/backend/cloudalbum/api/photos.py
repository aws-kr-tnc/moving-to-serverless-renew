"""
    cloudalbum/api/photos.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    REST API for photos

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import os, uuid
from flask import current_app as app, make_response
from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pathlib import Path
from jsonschema.exceptions import ValidationError
from cloudalbum import db
from cloudalbum.database.models import Photo
from cloudalbum.schemas import validate_photo_info
from cloudalbum.util.file_control import email_normalize, delete, save, insert_basic_info
from werkzeug.exceptions import BadRequest, InternalServerError


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
file_upload_parser.add_argument('nation', type=str, location='form')
file_upload_parser.add_argument('address', type=str, location='form')


@api.route('/ping')
@api.doc('photos ping!')
class Ping(Resource):
    @api.doc(responses={200: 'pong success'})
    @jwt_required
    def get(self):
        app.logger.debug('success:pong!')
        return make_response({'ok': True, 'Message': 'pong'}, 200)


@api.route('/file')
@api.expect(file_upload_parser)
class FileUpload(Resource):
    @jwt_required
    def post(self):
        form = file_upload_parser.parse_args()
        filename_orig = form['file'].filename
        extension = (filename_orig.rsplit('.', 1)[1]).lower()
        current_user = get_jwt_identity()

        if extension.lower() not in ['jpg', 'jpeg', 'bmp', 'gif', 'png']:
            app.logger.error('File format is not supported:{0}'.format(filename_orig))
            raise BadRequest('File format is not supported:{0}'.format(filename_orig))

        try:
            filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
            filesize = save(form['file'], filename, current_user['email'])
            insert_basic_info(current_user['user_id'], filename, filename_orig, filesize, form)
            committed = Photo.query.filter_by(user_id=current_user['user_id'],
                                              filename=filename,
                                              filename_orig=filename_orig).first()
            return make_response({'ok': True, "photo_id": committed.id}, 200)
        except Exception as e:
            app.logger.error('File upload failed:user_id:{0}: {1}'.format(get_jwt_identity()['user_id'], e))
            raise InternalServerError('File upload failed: {0}'.format(e))


@api.route('/<photo_id>/info')
@api.doc('upload a photo information with photo_id')
class InfoUpload(Resource):
    @api.doc(responses={200: 'success photo information upload',
                        500: 'internal server error'})
    @api.expect(photo_info)
    @jwt_required
    def post(self, photo_id):
        """update photo additional information"""
        infos_column = ['tags', 'desc', 'model', 'geotag_lat', 'geotag_lng', 'make',
                        'width', 'height', 'city', 'nation', 'address']
        body = request.get_json()
        try:
            valid_data = validate_photo_info(body)['data']
            photo = Photo.query.filter_by(id=photo_id).first()

            for key in infos_column:
                if key not in valid_data.keys():
                    valid_data[key] = None

            photo.taken_date = datetime.strptime(valid_data['taken_date'], "%Y:%m:%d %H:%M:%S")
            photo.id = photo_id
            photo.tags = valid_data['tags']
            photo.desc = valid_data['desc']
            photo.geotag_lat = valid_data['geotag_lat']
            photo.geotag_lng = valid_data['geotag_lng']
            photo.make = valid_data['make']
            photo.model = valid_data['model']
            photo.width = valid_data['width']
            photo.height = valid_data['height']
            photo.city = valid_data['city']
            photo.nation = valid_data['nation']
            photo.address = valid_data['address']
            db.session.add(photo)
            db.session.commit()
            app.logger.debug('success:photo info update:{}'.format(valid_data))
            return make_response({'ok': True, 'photos': photo.to_json()}, 200)
        except ValidationError as e:
            app.logger.error('Photo information format is wrong: {}'.format(body))
            app.logger.error(e)
            raise BadRequest('Photo information format is wrong')
        except Exception as e:
            app.logger.error('Photo information update failed:{}'.format(body))
            app.logger.error(e)
            raise InternalServerError('Photo information update failed: {0}'.format(e))


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
            current_user = get_jwt_identity()['user_id']
            photos = [photo.to_json() for photo in Photo.query.filter_by(user_id=current_user)]
            app.logger.debug('success:photos_list: {0}'.format(photos))
            return make_response({'ok': True, 'photos': photos}, 200)
        except Exception as e:
            app.logger.error('Photos list retrieving failed')
            app.logger.error(e)
            raise InternalServerError('Photos list retrieving failed')


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
        user = get_jwt_identity()

        try:
            db_photo = Photo.query.filter_by(id=photo_id).first()
            if db_photo is None:
                app.logger.error('Not exist photo_id: {}'.format(photo_id))
                raise BadRequest('Not exist photo_id')
            filename = db_photo.filename
            db.session.delete(db_photo)
            db.session.commit()
            file_deleted = delete(filename, user['email'])

            if file_deleted:
                app.logger.debug("success:photo deleted: photo_id:{}".format(photo_id))
                return make_response({'ok': True, 'photos': {'photo_id': photo_id}}, 200)
            else:
                raise FileNotFoundError('File not found error')
        except BadRequest as e:
            raise BadRequest(e)
        except FileNotFoundError as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)

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
            email = get_jwt_identity()['email']
            path = os.path.join(app.config['UPLOAD_FOLDER'], email_normalize(email))
            full_path = Path(path)

            photo = db.session.query(Photo).filter_by(id=photo_id).first()

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

