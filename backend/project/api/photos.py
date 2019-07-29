
from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc
from project import db
from project.api.models import User

photos_blueprint = Blueprint('photos', __name__)
api = Api(photos_blueprint)


class PhotosPing(Resource):
    def get(self):
        return {
        'status': 'success',
        'message': 'pong!'
    }


api.add_resource(PhotosPing, '/photos/ping')

