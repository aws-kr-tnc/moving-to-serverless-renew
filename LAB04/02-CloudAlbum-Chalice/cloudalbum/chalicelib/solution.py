import boto3


def solution_get_parameter_from_parameter_store(param_name):
    ssm = boto3.client('ssm')

    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[param_name, ], WithDecryption=True
    )
    return response