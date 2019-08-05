
from flask import Blueprint, request
from flask_restplus import Api, Resource, fields
from sqlalchemy import exc
from project import db
from project.api.models import User
import json
from project.util.response import default_response, response_with_msg, response_with_data, response_with_msg_data

photos_blueprint = Blueprint('photos', __name__)
api = Api(photos_blueprint, doc='/swagger/', title='Photos', description='CloudAlbum-photos: \n prefix url "/photos" is already exist.', version='0.1')

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




