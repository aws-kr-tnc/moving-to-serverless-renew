
from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc



map_blueprint = Blueprint('map', __name__)
api = Api(map_blueprint)


class MapPing(Resource):
    def get(self):
        return {
        'status': 'success',
        'message': 'pong!'
    }


api.add_resource(MapPing, '/map/ping')

