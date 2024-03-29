"""
    cloudalbum/util/file_control.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Handling image files which uploaded by user.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
from io import BytesIO
from flask import current_app as app
from PIL import Image
from pathlib import Path
from aws_xray_sdk.core import xray_recorder
from cloudalbum.solution import solution_put_object_to_s3, solution_generate_s3_presigned_url
from cloudalbum.database.model_ddb import Photo, photo_deserialize
from datetime import datetime
import os
import boto3


def email_normalize(email):
    return email.replace('@', '_at_').replace('.', '_dot_')


def make_thumbnail(path, filename):
    """
    Generate thumbnail from original image file.
    :param path: pathlib.Path, which pointing a original file directory
    :param filename: secure file name
    :return: None
    """
    thumb_path = path / 'thumbnails'
    thumb_file_location = thumb_path / filename

    try:
        if not thumb_path.exists():
            thumb_path.mkdir()
            app.logger.info("Create folder for thumbnails: %s", str(thumb_path))

        im = Image.open(path / filename)
        im = im.convert('RGB')
        im.thumbnail((300, 200, Image.ANTIALIAS))
        im.save(thumb_file_location)
        app.logger.debug("success:thumbnail saved!:{}".format(str(thumb_file_location)))
    except Exception as e:
        app.logger.error("ERROR:Thumbnails creation error:{}".format(str(thumb_file_location)))
        app.logger.error(e)


@xray_recorder.capture()
def make_thumbnails_s3(file_p):
    result_bytes_stream = BytesIO()

    try:
        im = Image.open(file_p)
        im = im.convert('RGB')
        im.thumbnail((app.config['THUMBNAIL_WIDTH'], app.config['THUMBNAIL_HEIGHT'], Image.ANTIALIAS))
        im.save(result_bytes_stream, 'JPEG')
    except Exception as e:
        app.logger.debug(e)

    return result_bytes_stream.getvalue()


def delete(filename, email):
    """
    Delete specific file (with thumbnail)
    :param photo: specific photo ORM object
    :param email: registered user email
    :return: Boolean
    """
    try:
        base_path = Path(app.config['UPLOAD_DIR']) / email_normalize(email)
        thumbnail_file_location = base_path / 'thumbnails' / filename
        original_file_location = base_path / filename

        if thumbnail_file_location.exists():
            Path.unlink(thumbnail_file_location)
            app.logger.debug('success:thumbnail file deleted:filepath:{}'.format(thumbnail_file_location))
        else:
            app.logger.debug('DEBUG:thumbnail file not exist:filepath:{}'.format(thumbnail_file_location))

        if original_file_location.exists():
            Path.unlink(original_file_location)
            app.logger.debug('success:original file deleted:filepath:{}'.format(original_file_location))
            return True
        else:
            app.logger.debug('DEBUG:original file not exist:filepath:{}'.format(original_file_location))
            return True

    except Exception as e:
        app.logger.error('Error occurred while deleting file:filename:{0}:email:{1}'.format(filename, email))
        app.logger.error(e)
        raise e


@xray_recorder.capture()
def delete_s3(filename, email):
    prefix = "photos/{0}/".format(email_normalize(email))
    prefix_thumb = "photos/{0}/thumbnails/".format(email_normalize(email))

    key = "{0}{1}".format(prefix, filename)
    key_thumb = "{0}{1}".format(prefix_thumb, filename)

    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=app.config['S3_PHOTO_BUCKET'], Key=key)
        s3_client.delete_object(Bucket=app.config['S3_PHOTO_BUCKET'], Key=key_thumb)
        app.logger.debug("success:s3 file delete done:{}".format(filename))
        return True
    except Exception as e:
        app.logger.error('ERROR:deleting file from s3 failed:%s', e)
        raise e


def save(upload_file, filename, email):
    """
    Upload input file (photo) to specific path for individual user.
    Save original file and thumbnail file.
    :param upload_file: file object
    :param filename: secure filename for upload
    :param email: user email address
    :param app: Flask.application
    :return: file size (byte)
    """
    path = Path(app.config['UPLOAD_DIR']) / email_normalize(email)

    try:
        if not path.exists():
            path.mkdir()
            app.logger.info("folder created:{}".format(str(path)))

        original_full_path = path / filename
        upload_file.save(str(original_full_path))
        app.logger.debug("success:original file saved!:{}".format(str(original_full_path)))
        file_size = os.stat(original_full_path).st_size

        make_thumbnail(path, filename)

        return file_size
    except Exception as e:
        app.logger.debug("ERROR:failed file saving:original or thumbnail: {}".format(filename))
        app.logger.error(e)
        raise e


@xray_recorder.capture()
def save_s3(upload_file_stream, filename, email):
    prefix = "photos/{0}/".format(email_normalize(email))
    prefix_thumb = "photos/{0}/thumbnails/".format(email_normalize(email))

    key = "{0}{1}".format(prefix, filename)
    key_thumb = "{0}{1}".format(prefix_thumb, filename)

    s3_client = boto3.client('s3')
    original_bytes = upload_file_stream.stream.read()

    try:
        solution_put_object_to_s3(s3_client, key, original_bytes)

        app.logger.debug('success: s3://{0}/{1} uploaded'.format(app.config['S3_PHOTO_BUCKET'], key))

        # Save thumbnail file
        upload_file_stream.stream.seek(0)
        solution_put_object_to_s3(s3_client, key_thumb, make_thumbnails_s3(upload_file_stream))

        app.logger.debug('s3://{0}/{1} uploaded'.format(app.config['S3_PHOTO_BUCKET'], key_thumb))

        return len(original_bytes)
    except Exception as e:
        app.logger.error('Error occurred while saving file to S3:%s', e)
        raise e


@xray_recorder.capture()
def presigned_url(filename, email, Thumbnail=True):

    try:
        s3_client = boto3.client('s3', config=boto3.session.Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
        key = None
        if Thumbnail:
            key = "photos/{0}/thumbnails/{1}".format(email_normalize(email), filename)
        else:
            key = "photos/{0}/{1}".format(email_normalize(email), filename)

        url = solution_generate_s3_presigned_url(s3_client, key)
        return url


    except Exception as e:
        app.logger.error('ERROR:creating presigned url failed:{0}'.format(e))
        raise e


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
        s3_client = boto3.client('s3', config=boto3.session.Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
        thumb_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': app.config['S3_PHOTO_BUCKET'], 'Key': key_thumb},
            ExpiresIn=app.config['S3_PRESIGNED_URL_EXPIRE_TIME'])
        origin_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': app.config['S3_PHOTO_BUCKET'], 'Key': key_origin},
            ExpiresIn=app.config['S3_PRESIGNED_URL_EXPIRE_TIME'])
    except Exception as e:
        raise e
    return thumb_url, origin_url


def with_presigned_url(current_user, photo):
    """
    Append additional attributes for presigned URL access.
    :param current_user:
    :param photo:
    :return:
    """
    thumbSrc, originalSrc = presigned_url_both(photo.filename, current_user['email'])
    temp = {}
    temp['address'] = photo.address
    temp['city'] = photo.city
    temp['desc'] = photo.desc
    temp['filename'] = photo.filename
    temp['filename_orig'] = photo.filename_orig
    temp['filesize'] = photo.filesize
    temp['geotag_lat'] = float(photo.geotag_lat)
    temp['geotag_lng'] = float(photo.geotag_lng)
    temp['height'] = photo.height
    temp['id'] = photo.id
    temp['make'] = photo.make
    temp['model'] = photo.model
    temp['nation'] = photo.nation
    temp['tags'] = photo.tags
    temp['taken_date'] = photo.taken_date
    temp['upload_date'] = photo.upload_date
    temp['user_id'] = photo.user_id
    temp['width'] = photo.width
    temp['thumbSrc'] = thumbSrc
    temp['originalSrc'] = originalSrc
    return temp
