from flask import current_app as app
from werkzeug.security import generate_password_hash

from cloudalbum.db.model_ddb import User
from cloudalbum.util.config import conf


def solution_put_new_user(new_user_id, user_data):
    # print(
    #     "\nRUNNING SOLUTION CODE:",
    #     "Put new signup user information!",
    #     "Follow the steps in the lab guide to replace this method with your own implementation.")

    user = User(new_user_id)
    user.email = user_data['email']
    user.password = generate_password_hash(user_data['password'])
    user.username = user_data['username']
    user.photos = []
    user.save()



def solution_get_user_data_with_idx(signin_data):
    # print(
    #     "\nRUNNING SOLUTION CODE:",
    #     "Get user data with email which is Global Secondary Index",
    #     "Follow the steps in the lab guide to replace this method with your own implementation.")

    db_user = None
    for item in User.email_index.query(signin_data['email']):
        if item is not None:
            db_user = item
    return db_user

def solution_put_photo_info_ddb(user_id, new_photo):
    # print(
    #     "\nRUNNING SOLUTION CODE:",
    #     "Update Photo informtation into User table!",
    #     "Follow the steps in the lab guide to replace this method with your own implementation.")

    try:
        User(id=user_id).update(
            actions=[
                User.photos.set((User.photos | []).append([new_photo]))
            ]
        )
        app.logger.debug('success:create photo into ddb: user_id:{}, photo_id:{}'.format(user_id, new_photo.id))
    except Exception as e:

        app.logger.error(e)
        raise e


def solution_delete_photo_from_ddb(user, photos, photo):
    # print(
    #     "\nRUNNING SOLUTION CODE:",
    #     "Delete a photo from photos list, and update!",
    #     "Follow the steps in the lab guide to replace this method with your own implementation.")
    try:
        photos.remove(photo)
        User(id=user['user_id']).update(
            actions=[
                User.photos.set(photos)
            ]
        )
        app.logger.debug("success:delete photo from ddb: userid:{}, photo_id:{}".format(user['user_id'], photo.id))
    except Exception as e:
        app.logger.error("ERROR:delete photo from ddb failed: userid:{}, photo_id:{}".format(user['user_id'], photo.id))
        app.logger.error(e)
        raise e

def solution_put_object_to_s3(s3_client, key, upload_file_stream):
    print(
        "\nRUNNING TODO#5 SOLUTION CODE:",
        "Put object into S3 bucket!",
        "Follow the steps in the lab guide to replace this method with your own implementation.")
    try:
        s3_client.put_object(
            Bucket=conf['S3_PHOTO_BUCKET'],
            Key=key,
            Body=upload_file_stream,
            ContentType='image/jpeg',
            StorageClass='STANDARD'
        )
        app.logger.debug('success:put object into s3:key:{}'.format(key))

    except Exception as e:
        app.logger.error('ERROR:failed put object: key:{}'.format(key))
        app.logger.error(e)
        raise e


def solution_generate_s3_presigned_url(s3_client, key):
    print(
        "\nRUNNING TODO#6 SOLUTION CODE:",
        "Create S3 object presigned url!",
        "Follow the steps in the lab guide to replace this method with your own implementation.")
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': conf['S3_PHOTO_BUCKET'],
                'Key': key})
    return url

