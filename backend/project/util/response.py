import copy

dic_default_response = {
    200: { 'code': 200,
            'message': 'Ok'},
    201 : { 'code': 201,
            'message': 'Created'},
    400 : { 'code': 400,
            'message': 'Bad request'},
    404 : { 'code': 404,
            'message':'Not found'},
    405 : { 'code': 405,
            'message':'Method not allowed'},
    500 : { 'code': 500,
            'message': 'Internal server error'}
                 }

def default_response(code):
    try:
        if code in dic_default_response:
            return dic_default_response[code], code
        else:
            raise ValueError
    except:
        raise ValueError

def response_with_msg(code, msg):
    try:
        if code in dic_default_response:
            res = copy.deepcopy(dic_default_response[code])
            res['message'] = msg
            return res, code
        else:
            raise ValueError
    except:
        # app.logger.debug("Undefined error: %s" % code)
        raise ValueError

def response_with_data(code, data):
    try:
        if code in dic_default_response:
            res = copy.deepcopy(dic_default_response[code])
            # res['message'] = msg
            res['data'] = data
            return res, code
        else:
            raise ValueError
    except:
        # app.logger.debug("Undefined error: %s" % code)
        raise ValueError

def response_with_msg_data(code, msg, data):
    try:
        if code in dic_default_response:
            res = copy.deepcopy(dic_default_response[code])
            res['message'] = msg
            res['data'] = data
            return res, code
        else:
            raise ValueError
    except:
        # app.logger.debug("Undefined error: %s" % code)
        raise ValueError