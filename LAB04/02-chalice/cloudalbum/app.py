from chalice import Response
from chalice import Chalice
from chalicelib import util
import logging
import boto3

app = Chalice(app_name='cloudalbum')


@app.route('/users/signin', methods=['POST'])
def signin():
    return {'name': 'hong gil dong'}


@app.route('/users/signup', methods=['POST'], content_types=['application/json'])
def signup():
    app.log.debug(app.current_request.json_body)
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
