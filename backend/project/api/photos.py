from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from project import db
from project.api.models import Photo
from datetime import datetime
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data
from flask_login import current_user


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
    'id' : fields.Integer,
    'email' : fields.String,
    'tags' : fields.String,
    'desc' : fields.String,
    'filename_orig' : fields.String,
    'filename' : fields.String,
    'filesize': fields.Integer,
    'geotag_lat' : fields.Float,
    'geotag_lng' : fields.Float,
    'upload_date' : fields.DateTime,
    'taken_date' : fields.DateTime,
    'make' : fields.String,
    'model' : fields.String,
    'width' : fields.String,
    'height' : fields.String,
    'city' : fields.String,
    'nation'  : fields.String,
    'address' : fields.String
})


# upload a photo file
@api.route('/new')
@api.doc('upload a photo')
class Upload(Resource):
    # @api.marshal_with(response)
    @api.doc(responses={200: 'success photo upload',
                        500: 'internal server error'})
    @api.expect(new_photo)
    def post(self):
        body = request.get_json()
        user_id = current_user.id
        taken_date = datetime.strptime(body['taken_date'], "%Y:%m:%d %H:%M:%S")
        photo = Photo(user_id= user_id,
                      tags = body['tags'],
                      desc = body['desc'],
                      filename_orig= body['filename_orig'],
                      filename= body['filename'],
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

        return response_with_msg(200, "pong!")

# return file data list
# photo delete
# photo url
# photo edit
# map view



