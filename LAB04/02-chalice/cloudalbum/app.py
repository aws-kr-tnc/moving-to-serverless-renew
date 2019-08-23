from chalice import Response
from chalice import Chalice
from chalicelib import util
from chalicelib.config import conf
from chalicelib.cognito import signup_cognito
import boto3, logging, hmac, base64, hashlib, uuid


app = Chalice(app_name='cloudalbum')

app.debug = True
app.log.setLevel(logging.DEBUG)


@app.route('/users/signin', methods=['POST'])
def signin():
    return {'name': 'hong gil dong'}


@app.route('/users/signup', methods=['POST'], content_types=['application/json'])
def signup():
    user_data = app.current_request.json_body
    msg = '{0}{1}'.format(user_data['email'], conf['COGNITO_CLIENT_ID'])
    dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
                   msg=msg.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    try:
        signup_cognito(app, user_data, dig)
    except Exception as e:
        app.log.error(e)

    return {'name': 'hong gil dong'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
