from flask import Blueprint, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from project import db
from project.api.models import Photo, User
from datetime import datetime
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
from werkzeug.datastructures import FileStorage
from flask import current_app as app
from werkzeug.utils import secure_filename
from project.schemas import validate_photo_info
from flask_jwt_extended import (create_access_token, create_refresh_token, JWTManager,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from project.api.users import Signin as user_signin

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

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',type=FileStorage, required=True)

response = api.model('Response', {
    'code': fields.Integer,
    'message':fields.String,
    'data':fields.String
})

photo_info = api.model('New_photo', {
    'tags' : fields.String,
    'desc' : fields.String,
    'geotag_lat' : fields.Float,
    'geotag_lng' : fields.Float,
    'taken_date' : fields.DateTime("%Y:%m:%d %H:%M:%S"),
    'make' : fields.String,
    'model' : fields.String,
    'width' : fields.String,
    'height' : fields.String,
    'city' : fields.String,
    'nation'  : fields.String,
    'address' : fields.String
})


def save(upload_file, filename, email):
    """
    Upload input file (photo) to specific path for individual user.
    Save original file and thumbnail file.
    :param upload_file: file object
    :param filename: secure filename for upload
    :param email: user email address
    :param app: Flask.application
    :return: file size (byte)
    """
    email_normalized = email.replace('@', '_at_').replace('.', '_dot_')
    path = os.path.join('/tmp/', email_normalized)

    try:
        if not os.path.exists(path):
            os.makedirs(path)
            app.logger.info("Create folder: %s", path)

        original_full_path = os.path.join(path, filename)
        upload_file.save(original_full_path)
        file_size = os.stat(original_full_path).st_size
        # make_thumbnails(path, filename, app)

    except Exception as e:
        app.logger.error('Error occurred while saving file:%s', e)
        raise e

    return file_size

def insert_basic_info(user_id, filename, filename_orig, filesize):

    new_photo = Photo(user_id=user_id,
                      filename=filename,
                      filename_orig=filename_orig,
                      filesize=filesize,
                      upload_date=datetime.today())
    db.session.add(new_photo)
    db.session.commit()

@api.route('/ping')
@api.doc('photos ping!')
class Ping(Resource):
    @api.doc(responses={ 200 : 'pong success'})
    @jwt_required
    def get(self):
        return make_response(jsonify({'ok':True, 'data':{'msg':'pong!'}}))




@api.route('/file')
@api.expect(upload_parser)
class FileUpload(Resource):
    @jwt_required
    def post(self):
        uploaded_file = upload_parser.parse_args()['file']
        filename_orig = uploaded_file.filename
        current_user = get_jwt_identity()

        extension = (filename_orig.rsplit('.', 1)[1]).lower()
        filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
        filesize = save(uploaded_file, filename, current_user['email'])

        user_id = current_user['user_id']
        insert_basic_info(user_id, filename, filename_orig, filesize)

        committed = Photo.query.filter_by(user_id=user_id, filename=filename, filename_orig=filename_orig).first()

        return response_with_msg_data(200, 'file uploaded', {"photo_id":committed.id})

# upload a photo file
@api.route('/<photo_id>/info')
@api.doc('upload a photo information with photo_id')
class InfoUpload(Resource):
    @api.doc(responses={200: 'success photo information upload',
                        500: 'internal server error'})
    @api.expect(photo_info)
    @jwt_required
    def post(self, photo_id):

        if validate_photo_info(request.get_json())['ok']:
            body = request.get_json()
            try:
                photo = Photo.query.filter_by(id=photo_id).first()

                photo.taken_date = datetime.strptime(body['taken_date'], "%Y:%m:%d %H:%M:%S")
                photo.id= photo_id
                photo.tags = body['tags']
                photo.desc = body['desc']
                photo.geotag_lat = body['geotag_lat']
                photo.geotag_lng= body['geotag_lng']
                photo.make= body['make']
                photo.model= body['model']
                photo.width= body['width']
                photo.height= body['height']
                photo.city= body['city']
                photo.nation= body['nation']
                photo.address= body['address']

                db.session.commit()
                app.logger.debug('success:photo info update:{}'.format(body))
                return response_with_msg(200, "file uploaded")
            except Exception as e:
                app.logger.debug('ERROR:photo info update:{}'.format(body))
                app.logger.debug(e)
                return default_response(500)
        else:
            app.logger.debug('ERROR:photo info update:{}'.format(request.get_json()))
            return default_response(400)

@api.route('/')
class List(Resource):
    @api.doc(
        responses=
            {
                200:"Return the whole photos list",
                500: "Internal server error"
            }
        )
    @jwt_required
    def get(self):
        """Get all photos as list"""
        try:
            photos = [photo.to_json() for photo in Photo.query.all()]
            data = {
                'photos': photos
            }
            app.logger.debug("success:photos_list:%s" % photos)


            return make_response(jsonify({'ok': True, 'data': data}), 200)
        except:
            app.logger.debug("photos list failed:users list:%s" % photos)
            return make_response(jsonify({'ok': False, 'data': data}), 500)

# photo delete
# photo url
# photo edit
