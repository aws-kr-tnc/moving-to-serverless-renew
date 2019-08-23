from chalice import Response
from chalice import Chalice
from chalicelib import util
import logging
import boto3

app = Chalice(app_name='cloudalbum')



@app.route('/', methods=['GET'])
def signin():
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html

    cognito_login = "https://{0}/"\
                    "login?response_type=code&client_id={1}"\
                    "&state={2}"\
                    "&redirect_uri={3}/callback".format(
                        conf['COGNITO_DOMAIN'],
                        conf['COGNITO_CLIENT_ID'],
                        uuid.uuid4().hex,
                        conf['BASE_URL'])

    app.log.debug(cognito_login)

    return Response(
        status_code=301,
        headers={'Location': cognito_login},
        body=''
    )




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
