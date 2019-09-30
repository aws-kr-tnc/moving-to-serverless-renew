"""
    cloudalbum/chalicelib/cognito.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Configurations for application.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import boto3
from chalice import CORSConfig
from aws_parameter_store import AwsParameterStore


def get_param_path(param_path):
    """
    Retrieve all key:values in the Parameter Store.
    :param param_path:
    :return:
    """
    region = boto3.session.Session().region_name
    store = AwsParameterStore(region)
    return store.get_parameters_dict(param_path)


# store configuration values for Cloudalbum
conf = get_param_path('/cloudalbum/')


def get_param(param_name):
    """
    This function reads a secure parameter from AWS' SSM service.
    The request must be passed a valid parameter name, as well as
    temporary credentials which can be used to access the parameter.
    The parameter's value is returned.
    """
    # Create the SSM Client
    ssm = boto3.client('ssm')

    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[param_name, ], WithDecryption=True
    )

    # Store the credentials in a variable
    result = response['Parameters'][0]['Value']
    return result


cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['*'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)
