from flask import current_app as app
from PIL import Image
from pathlib import Path

from cloudalbum.util.config import conf
from cloudalbum.db.model_ddb import User, Photo, photo_deserialize

import os
from datetime import datetime



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


def delete(filename, email):
    """
    Delete specific file (with thumbnail)
    :param photo: specific photo ORM object
    :param email: registered user email
    :return: Boolean
    """
    try:
        base_path = Path(conf['UPLOAD_DIR']) / email_normalize(email)
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
    path = Path(conf['UPLOAD_DIR']) / email_normalize(email)

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



def create_photo_info(filename, filesize, form):
    new_photo = Photo(id=filename,
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

    app.logger.debug('new_photo: {0}'.format(photo_deserialize(new_photo)))
    return new_photo
