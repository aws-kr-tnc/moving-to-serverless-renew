import boto3
import base64
from chalicelib.config import conf


def signup_confirm(id):
    client = boto3.client('cognito-idp')
    client.admin_confirm_sign_up(
        UserPoolId=conf['COGNITO_POOL_ID'],
        Username=id
    )


def signup_cognito(app, user, dig):
    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId=conf['COGNITO_CLIENT_ID'],
        SecretHash=base64.b64encode(dig).decode(),
        Username=user['email'],
        Password=user['password'],
        UserAttributes=[
            {
                'Name': 'name',
                'Value': user['username']
            }
        ],
        ValidationData=[
            {
                'Name': 'name',
                'Value': user['username']
            }
        ]

    )

    email = response['CodeDeliveryDetails']['Destination']
    id = response['UserSub']

    # automatically confirm user for lab
    signup_confirm(id)
    return {'email': email, 'id': id}




