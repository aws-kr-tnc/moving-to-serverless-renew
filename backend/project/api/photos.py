from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from project import db
from project.api.models import Photo
from datetime import datetime
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
from flask_login import current_user, login_required
from werkzeug.datastructures import FileStorage
from flask import current_app as app
from werkzeug.utils import secure_filename
from project.api.users import Signin as user_signin

import os, re, uuid

photos_blueprint = Blueprint('photos', __name__)
api = Api(photos_blueprint, doc='/swagger/',
                            title='Photos',
                            description='CloudAlbum-photos: \n prefix url "/photos" is already exist.',
                            version='0.1')


response = api.model('Response', {
    'code': fields.Integer,
    'message':fields.String,
    'data':fields.String
})


@api.route('/ping')
@api.doc('photos ping!')
class PhotosPing(Resource):
    @api.marshal_with(response)
    @api.doc(responses={ 200 : 'pong success'})
    def get(self):
        return response_with_msg(200, "pong!")


new_photo = api.model('New_photo', {

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


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',type=FileStorage, required=True)

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
def insert_new_photo(user_id, filename, filename_orig, filesize):

    new_photo = Photo(user_id=user_id,
                      filename=filename,
                      filename_orig=filename_orig,
                      filesize=filesize,
                      upload_date=datetime.today())
    db.session.add(new_photo)
    db.session.commit()

@api.route('/file')
@api.expect(upload_parser)
class FileUpload(Resource):
    @login_required
    def post(self):
        uploaded_file = upload_parser.parse_args()['file']
        filename_orig = uploaded_file.filename

        extension = (filename_orig.rsplit('.', 1)[1]).lower()
        filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
        filesize = save(uploaded_file, filename, current_user.email)

        user_id = current_user.id
        insert_new_photo(user_id, filename, filename_orig, filesize)

        committed = Photo.query.filter_by(user_id=user_id, filename=filename, filename_orig=filename_orig).first()

        return response_with_msg_data(200, 'file uploaded', {"photo_id":committed.id})

# upload a photo file
@api.route('/<photo_id>/info')
@api.doc('upload a photo information with photo_id')
class UploadPhotoInfo(Resource):
    @api.doc(responses={200: 'success photo information upload',
                        500: 'internal server error'})
    @api.expect(new_photo)
    @login_required
    def post(self, photo_id):
        body = request.get_json()
        user_id = current_user.id

        # extension = (body['filename_orig'].rsplit('.', 1)[1]).lower()
        # filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
        # taken_date = datetime.strptime(body['taken_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

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
        # db.session.add(photo)
        db.session.commit()

        return response_with_msg(200, "file uploaded")

@api.route('/')
class PhotosList(Resource):
    @api.doc(
        responses=
            {
                200:"Return the whole photos list",
                500: "Internal server error"
            }
        )
    def get(self):
        """Get all photos as list"""
        try:
            photos = [photo.to_json() for photo in Photo.query.all()]
            data = {
                'photos': photos
            }
            app.logger.debug("success:photos_list:%s" % photos)

            return response_with_data(200, data)
        except:
            app.logger.debug("photos list failed:users list:%s" % photos)
            return default_response(500)

# return file data list
# photo delete
# photo url
# photo edit


signin_user = api.model ('Signin_user',{
    'email': fields.String,
    'password':fields.String
})

@api.route('/signin')
class Signin(Resource):
    @api.expect(signin_user)
    def post(self):
        """to create session in swagger photos page"""
        return user_signin.post(Resource)