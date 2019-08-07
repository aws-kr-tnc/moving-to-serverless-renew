from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
from flask import app

user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


user_signin_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

photo_info_schema = {
    "type":'object',
    'properties': {
        'tags' : {"type":"string"},
        'desc' : {"type":"string"},
        'geotag_lat' : {"type":"number"},
        'geotag_lng' : {"type":"number"},
        'taken_date' : {
            "type":"string",
            "format": "date-time"},
        'make' : {"type":"string"},
        'model' : {"type":"string"},
        'width' : {"type":"string"},
        'height' : {"type":"string"},
        'city' : {"type":"string"},
        'nation'  : {"type":"string"},
        'address' : {"type":"string"}
    }
}

def validate_photo_info(data):
    try:
        validate(data, photo_info_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_signin(data):
    try:
        validate(data, user_signin_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

