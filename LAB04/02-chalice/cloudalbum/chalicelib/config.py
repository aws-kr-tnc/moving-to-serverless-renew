from chalice import CORSConfig
from aws_parameter_store import AwsParameterStore
import boto3


def get_param_path(param_path):
    region = boto3.session.Session().region_name
    store = AwsParameterStore(region)
    return store.get_parameters_dict(param_path)


conf = get_param_path('/cloudalbum/')

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)

