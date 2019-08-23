# def cognito_signup(signup_user):
#     user = signup_user;
#     msg = '{0}{1}'.format(user['email'], conf['COGNITO_CLIENT_ID'])
#
#     dig = hmac.new(conf['COGNITO_CLIENT_SECRET'].encode('utf-8'),
#                    msg=msg.encode('utf-8'),
#                    digestmod=hashlib.sha256).digest()
#     try:
#         # TODO 7: Implement following solution code to sign up user into cognito user pool
#         return solution_signup_cognito(user, dig)
#
#     except Exception as e:
#         app.logger.error("ERROR: failed to enroll user into Cognito user pool")
#         app.logger.error(e)
