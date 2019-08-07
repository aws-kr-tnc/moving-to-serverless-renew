from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

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
        'tags' : {"type":"String"},
        'desc' : {"type":"String"},
        'geotag_lat' : {"type":"Numbers"},
        'geotag_lng' : {"type":"Numbers"},
        'taken_date' : {
            "type":"DateTime",
            "format": "%Y:%m:%d %H:%M:%S"},
        'make' : {"type":"String"},
        'model' : {"type":"String"},
        'width' : {"type":"String"},
        'height' : {"type":"String"},
        'city' : {"type":"String"},
        'nation'  : {"type":"String"},
        'address' : {"type":"String"}
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

