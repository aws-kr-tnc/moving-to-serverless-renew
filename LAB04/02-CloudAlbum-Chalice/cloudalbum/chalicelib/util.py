"""
    cloudalbum/chalicelib/util.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Utility functions

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""

import os
import cgi
import boto3
import pprint
from PIL import Image
from io import BytesIO
from chalicelib.config import conf
from chalice import ChaliceViewError

pp = pprint.PrettyPrinter(indent=2)


def get_parts(app):
    """
    Parse Multipart-form data
    :param app:
    :return:
    """
    rfile = BytesIO(app.current_request.raw_body)
    content_type = app.current_request.headers['content-type']
    _, parameters = cgi.parse_header(content_type)
    parameters['boundary'] = parameters['boundary'].encode('utf-8')
    parsed = cgi.parse_multipart(rfile, parameters)
    return parsed


def get_password_reset_url():
    """
    User password reset page provided by cognito.
    :return:
    """
    password_reset = "https://" \
                     "{0}/forgotPassword?response_type=code&client_id=" \
                     "{1}&redirect_uri=" \
                     "{2}" \
        .format(conf['COGNITO_DOMAIN'], conf['COGNITO_CLIENT_ID'],
                conf['BASE_URL'] + '/callback')
    return password_reset


def email_normalize(email):
    """
    Email normalization to get unique path.
    :param email: user email address.
    :return: normalized string value
    """
    return email.replace('@', '_at_').replace('.', '_dot_')


def make_thumbnails(path, filename, logger):
    """
    Generate thumbnail from original image file.
    :param path: target path
    :param filename: secure file name
    :param app: Falsk.application
    :return: None
    """
    thumb_full_path = '/tmp/thumbnail.jpg'

    im = Image.open(os.path.join(path, filename))
    logger.debug(os.path.join(path, filename))
    im = im.convert('RGB')
    im.thumbnail((int(conf['THUMBNAIL_WIDTH']), int(conf['THUMBNAIL_HEIGHT']), Image.ANTIALIAS))
    im.save(thumb_full_path)
    return thumb_full_path


def save_s3_chalice(bytes, filename, email, logger):
    """
    File save from multipart-form data.
    :param bytes:
    :param filename:
    :param email:
    :param logger:
    :return:
    """
    prefix = "photos/{0}/".format(email_normalize(email))
    prefix_thumb = "photos/{0}/thumbnails/".format(email_normalize(email))
    key = "{0}{1}".format(prefix, filename)
    key_thumb = "{0}{1}".format(prefix_thumb, filename)
    logger.debug('key: {0}'.format(key))
    logger.debug('key_thumb: {0}'.format(key_thumb))
    s3_client = boto3.client('s3')
    try:
        temp_file = '/tmp/' + filename
        with open(temp_file, 'wb') as f:
            f.write(bytes)
            statinfo = os.stat(temp_file)
            logger.debug(statinfo)
            s3_client.upload_file(temp_file, conf['S3_PHOTO_BUCKET'], key)
            thumb_path = make_thumbnails('/tmp', filename, logger)
            logger.debug('thumb_path for upload: {0}'.format(thumb_path))
            logger.debug('prefix_thumb: {0}'.format(prefix_thumb))
            logger.debug(os.stat(temp_file))
            s3_client.upload_file(thumb_path, conf['S3_PHOTO_BUCKET'], key_thumb)
    except Exception as e:
        logger.error('Error occurred while saving file:%s', e)
        raise ChaliceViewError('Error occurred while saving file.')
    return len(bytes)


def delete_s3(logger, filename, current_user):
    """
    Delete both original and thumbnail image file in the S3.
    :param logger:
    :param filename:
    :param current_user:
    :return:
    """
    prefix = "photos/{0}/".format(email_normalize(current_user['email']))
    prefix_thumb = "photos/{0}/thumbnails/".format(email_normalize(current_user['email']))
    key = "{0}{1}".format(prefix, filename)
    key_thumb = "{0}{1}".format(prefix_thumb, filename)
    logger.debug('Attempting delete object: {0}'.format(key))
    logger.debug('Attempting delete object: {0}'.format(key_thumb))
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_object(Bucket=conf['S3_PHOTO_BUCKET'], Key=key)
        s3_client.delete_object(Bucket=conf['S3_PHOTO_BUCKET'], Key=key_thumb)
    except Exception as e:
        logger.error('Error occurred while deleting file:%s', e)
        raise ChaliceViewError('Error occurred while deleting file.')


def presigned_url_both(filename, email):
    """
    Return presigned urls both original image url and thumbnail image url
    :param filename:
    :param email:
    :return:
    """
    prefix = "photos/{0}/".format(email_normalize(email))
    prefix_thumb = "photos/{0}/thumbnails/".format(email_normalize(email))
    key_thumb = "{0}{1}".format(prefix_thumb, filename)
    key_origin = "{0}{1}".format(prefix, filename)
    try:
        s3_client = boto3.client('s3')
        thumb_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': conf['S3_PHOTO_BUCKET'], 'Key': key_thumb},
            ExpiresIn=conf['S3_PRESIGNED_EXP'])
        origin_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': conf['S3_PHOTO_BUCKET'], 'Key': key_origin},
            ExpiresIn=conf['S3_PRESIGNED_EXP'])
    except Exception as e:
        raise ChaliceViewError(e)
    return thumb_url, origin_url


