"""
    cloudalbum/util/response.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Handling responses about user request.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import copy


dic_default_response = {
    200: {'code': 200,
          'message': 'Ok'},
    201: {'code': 201,
          'message': 'Created'},
    400: {'code': 400,
          'message': 'Bad request'},
    404: {'code': 404,
          'message': 'Not found'},
    405: {'code': 405,
          'message': 'Method not allowed'},
    500: {'code': 500,
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
        # application.logger.debug("Undefined error: %s" % code)
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
        # application.logger.debug("Undefined error: %s" % code)
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
        # application.logger.debug("Undefined error: %s" % code)
        raise ValueError
