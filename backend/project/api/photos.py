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
from flask_jwt_extended import jwt_required, get_jwt_identity
from PIL import Image
from pathlib import Path

import os, uuid

CONF_UPLOAD_DIR = '/tmp'

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


def email_normalized(email):
    return email.replace('@', '_at_').replace('.', '_dot_')


def make_thumbnail(path, filename):
    """
    Generate thumbnail from original image file.
    :param path: pathlib.Path, which pointing a original file directory
    :param filename: secure file name
    :return: None
    """
    thumb_path = path / 'thumbnails'
    thumb_file_location = thumb_path / filename

    try:
        if not thumb_path.exists():
            thumb_path.mkdir()
            app.logger.info("Create folder for thumbnails: %s", thumb_path._str)

        im = Image.open(os.path.join(path, filename))
        im = im.convert('RGB')
        im.thumbnail((300, 200, Image.ANTIALIAS))
        im.save(thumb_file_location)
        app.logger.debug("success:thumbnail saved!:{}".format(thumb_file_location._str))
    except Exception as e:
        app.logger.error("ERROR:Thumbnails creation error:{}:{}".format(thumb_file_location._str, e))
        raise e

def delete_file(filename, email):
    """
    Delete specific file (with thumbnail)
    :param photo: specific photo ORM object
    :param email: registered user email
    :return: Boolean
    """
    try:
        dir_location = '{0}/{1}'.format(CONF_UPLOAD_DIR, email_normalized(email))
        base_path = Path(dir_location)

        thumbnail_file_location = base_path / 'thumbnails' / filename
        original_file_location = base_path / filename

        if thumbnail_file_location.exists():
            Path.unlink(thumbnail_file_location)
        if original_file_location.exists():
            Path.unlink(original_file_location)
            return True
        else:
            app.logger.error('ERROR:delete failed:filepath:{}'.format(original_file_location))
            return False
    except Exception as e:
        app.logger.error('Error occurred while deleting file:%s', e)
        raise e


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
    path= Path(CONF_UPLOAD_DIR) / email_normalized(email)

    try:
        if not path.exists():
            path.mkdir()
            app.logger.info("Create folder:{}".format(path._str))

        original_full_path = path / filename
        upload_file.save(original_full_path._str)
        app.logger.debug("success:original file saved!:{}".format(original_full_path._str))
        file_size = os.stat(original_full_path).st_size

        make_thumbnail(path, filename)

        return file_size
    except Exception as e:
        app.logger.error('Error occurred while saving file:%s', e)


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


upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/file')
@api.expect(upload_parser)
class FileUpload(Resource):
    @jwt_required
    def post(self):
        try:
            uploaded_file = upload_parser.parse_args()['file']
            filename_orig = uploaded_file.filename
            current_user = get_jwt_identity()

            extension = (filename_orig.rsplit('.', 1)[1]).lower()
            filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
            filesize = save(uploaded_file, filename, current_user['email'])

            user_id = current_user['user_id']
            insert_basic_info(user_id, filename, filename_orig, filesize)

            committed = Photo.query.filter_by(user_id=user_id, filename=filename, filename_orig=filename_orig).first()
            return make_response({'ok': True, "photo_id": committed.id}, 200)
        except Exception as e:
            app.logger.error('ERROR:file upload failed:user_id:{}'.format(current_user['user_id']))
            app.logger.error(e)
            return make_response({'ok':False, 'data':{'user_id':current_user['user_id']}}, 500)


@api.route('/<photo_id>/info')
@api.doc('upload a photo information with photo_id')
class InfoUpload(Resource):
    @api.doc(responses={200: 'success photo information upload',
                        500: 'internal server error'})
    @api.expect(photo_info)
    @jwt_required
    def post(self, photo_id):
        """update photo additional information"""
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
                app.logger.error('ERROR:photo info update:{}'.format(body))
                app.logger.error(e)
                return default_response(500)
        else:
            app.logger.error('ERROR:photo info update:{}'.format(request.get_json()))
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
            app.logger.error("ERROR:photos list failed")
            return make_response(jsonify({'ok': False}), 500)



@api.route('/<photo_id>')
class OnePhoto(Resource):
    @api.doc(
        responses=
        {
            200: "Delete success",
            500: "Internal server error"
        }
    )
    @jwt_required
    def delete(self, photo_id):
        """one photo delete"""
        try:
            # DB에서 사진 정보 가지고 오기
            photo = Photo.query.filter_by(id=photo_id).first()
            filename = photo.filename

            # DB에서 사진정보 지우기
            db.session.delete(photo)
            db.session.commit()
            # 저장된 사진 지우기
            user = get_jwt_identity()
            file_deleted = delete_file(filename, user['email'])
            if file_deleted:
                return make_response({'ok':True, 'data':{'photo_id':photo_id}}, 200)
            else:
                raise FileNotFoundError
        except Exception as e:
            app.logger.error("ERROR:photo delete failed: photo_id:{}".format(photo_id))
            app.logger.error(e)
            return make_response({'ok':False, 'data':{'photo_id':photo_id}}, 500)

    get_parser = api.parser()
    get_parser.add_argument('mode', type=str, location='args')

    @api.doc(
        responses=
        {
            200: "Success",
            500: "Internal server error"
        }
    )
    @jwt_required
    @api.expect(get_parser)
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
            photo = db.session.query(Photo).filter_by(id=photo_id).first()
            path = os.path.join(CONF_UPLOAD_DIR, email_normalized(email))
            full_path = Path(path)
            if mode == "thumbnail":
                full_path = full_path / "thumbnails" / photo.filename
            else:
                full_path = full_path / photo.filename

            with full_path.open('rb') as f:
                contents = f.read()
                resp = make_response(contents)
            app.logger.debug("filepath:{}".format(full_path._str))
            resp.content_type = "image/jpeg"
            return resp
        except Exception as e:
            app.logger.error(e)
            return 'http://placehold.it/400x300'



# photo edit
