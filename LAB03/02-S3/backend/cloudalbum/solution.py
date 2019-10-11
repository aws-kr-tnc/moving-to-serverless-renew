"""
    cloudalbum/solution.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Hands-on lab solution file.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from datetime import datetime
from flask import current_app as app
from werkzeug.security import generate_password_hash
from cloudalbum.database.model_ddb import User, Photo


def solution_put_new_user(new_user_id, user_data):
    user = User(new_user_id)
    user.email = user_data['email']
    user.password = generate_password_hash(user_data['password'])
    user.username = user_data['username']
    user.save()


def solution_get_user_data_with_idx(signin_data):
    user_email = [item for item in User.email_index.query(signin_data['email'])]
    if not user_email:
        return None
    return user_email[0]


def solution_put_photo_info_ddb(user_id, filename, form, filesize):
    new_photo = Photo(id=filename,
                      user_id=user_id,
                      filename=filename,
                      filename_orig=form['file'].filename,
                      filesize=filesize,
                      upload_date=datetime.today(),
                      tags=form['tags'],
                      desc=form['desc'],
                      geotag_lat=form['geotag_lat'],
                      geotag_lng=form['geotag_lng'],
                      taken_date=datetime.strptime(form['taken_date'], "%Y:%m:%d %H:%M:%S"),
                      make=form['make'],
                      model=form['model'],
                      width=form['width'],
                      height=form['height'],
                      city=form['city'],
                      nation=form['nation'],
                      address=form['address'])
    new_photo.save()


def solution_delete_photo_from_ddb(user, photo_id):
    app.logger.info('RUNNING TODO#4 SOLUTION CODE:')
    app.logger.info('Delete a photo from photos list, and update!')
    app.logger.info('Follow the steps in the lab guide to replace this method with your own implementation.')

    photo = Photo.get(user['user_id'], photo_id)
    photo.delete()
    filename = photo.filename

    return filename


def solution_put_object_to_s3(s3_client, key, upload_file_stream):
    app.logger.info('RUNNING TODO#5 SOLUTION CODE:')
    app.logger.info('Put object into S3 bucket!')
    app.logger.info('Follow the steps in the lab guide to replace this method with your own implementation.')

    s3_client.put_object(
        Bucket=app.config['S3_PHOTO_BUCKET'],
        Key=key,
        Body=upload_file_stream,
        ContentType='image/jpeg',
        StorageClass='STANDARD'
    )

    app.logger.debug('success:put object into s3:key:{}'.format(key))


def solution_generate_s3_presigned_url(s3_client, key):
    app.logger.info('RUNNING TODO#6 SOLUTION CODE:')
    app.logger.info('Create S3 object presigned url!')
    app.logger.info('Follow the steps in the lab guide to replace this method with your own implementation.')
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': app.config['S3_PHOTO_BUCKET'],
                'Key': key},
        ExpiresIn=app.config['S3_PRESIGNED_URL_EXPIRE_TIME'])

    return url
