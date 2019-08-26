import copy
from flask import jsonify, make_response

def m_response(bool, data, code):
    return make_response({'ok': bool, 'photos': data}, code)

def err_response(bool, msg, code):
    return make_response({'ok':bool, 'Message':msg}, code)