from flask import make_response

def m_response(data, code):
    return make_response({'ok': True, 'photos': data}, code)

def err_response(msg, code):
    return make_response({'ok':False, 'Message':msg}, code)