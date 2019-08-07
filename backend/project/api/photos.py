from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from project import db
from project.api.models import Photo, User
from datetime import datetime
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
from flask_login import current_user, login_required, login_user
from werkzeug.datastructures import FileStorage
from flask import current_app as app
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

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
    'filename_orig' : fields.String,
    'filesize': fields.Integer,
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

@api.route('/file')
@api.expect(upload_parser)

class FileUpload(Resource):
    def post(self):
        body = api.payload
        filename = body.get('filename')

        args = upload_parser.parse_args()
        uploaded_file = args['file']

        save(uploaded_file, filename, current_user.email)

        return response_with_msg_data(200, 'file uploaded', {'filename':name})

# upload a photo file
@api.route('/fileinfo')
@api.doc('upload a photo')
# @login_required
class PhotoInfo(Resource):
    # @api.marshal_with(response)
    @api.doc(responses={200: 'success photo upload',
                        500: 'internal server error'})
    @api.expect(new_photo)
    def post(self):
        body = request.get_json()
        user_id = current_user.id
        extension = (body['filename_orig'].rsplit('.', 1)[1]).lower()
        filename = secure_filename("{0}.{1}".format(uuid.uuid4(), extension))
        taken_date = datetime.strptime(body['taken_date'], "%Y-%m-%dT%H:%M:%S.%fZ")

        photo = Photo(user_id= user_id,
                      tags = body['tags'],
                      desc = body['desc'],
                      filename_orig= body['filename_orig'],
                      filename= filename,
                      filesize= body['filesize'],
                      geotag_lat = body['geotag_lat'],
                      geotag_lng= body['geotag_lng'],
                      upload_date= datetime.today(),
                      taken_date= taken_date,
                      make= body['make'],
                      model= body['model'],
                      width= body['width'],
                      height= body['height'],
                      city= body['city'],
                      nation= body['nation'],
                      address= body['address']
                      )

        db.session.add(photo)
        db.session.commit()

        return response_with_msg_data(200, "file uploaded", {"filename": filename})

@api.route('/')
class UsersList(Resource):
    @api.doc(
        responses=
            {
                200:"Return the whole photos list",
                500: "Internal server error"

            }
        )
    @api.marshal_with(response)
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
# map view

signin_user = api.model ('Signin_user',{
    'email': fields.String,
    'password':fields.String
})

def data_validate(email, password):
    email_regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    if not re.match(email_regex, email) or (len(password) <= 1):
        return False
    return True

@api.route('/signin')
class Signin(Resource):
    @api.doc(responses={
        200:'login success',
        400: 'Invalidate data',
        500: 'Internal server error'
    })
    @api.expect(signin_user)
    @api.marshal_with(response)
    def post(self):
        """user signin"""
        try:
            post_data = request.get_json()

            if not post_data:
                app.logger.debug("ERROR:user signin:posted data is null")
                return default_response(400)

            email = post_data.get('email')
            password = post_data.get('password')

            if not data_validate(email, password):
                app.logger.debug("ERROR:user signin:invalidate data:%s" % post_data)
                return response_with_msg(400, 'email or password not valid')

            db_user = db.session.query(User).filter_by(email=email).first()

            if db_user and check_password_hash(db_user.password, password):
                login_user(db_user)
                app.logger.debug("success:user signin:id: %s | email: %s" % (db_user.id, db_user.email))
                return response_with_msg(200, "Login Success!")
            else:
                app.logger.debug('ERROR:user signin failed:password unmatched:%s' % db_user)
                return response_with_msg(400, "Login Failed")
        except:
            app.logger.debug('ERROR:user signin failed:unknown issue:%s' % db_user)
            return default_response(500)



