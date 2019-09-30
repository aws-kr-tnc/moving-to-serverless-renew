"""
    cloudalbum/chalicelib/model_ddb.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    Data model class for Photos table.

    :description: CloudAlbum is a fully featured sample application for 'Moving to AWS serverless' training course
    :copyright: © 2019 written by Dayoungle Jun, Sungshik Jou.
    :license: MIT, see LICENSE for more details.
"""
import json
from datetime import datetime
from tzlocal import get_localzone
from pynamodb.models import Model
from chalicelib.config import conf
from chalicelib.util import presigned_url_both
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class Photo(Model):
    """
    Photo table for DynamoDB
    """

    class Meta:
        table_name = 'Photo'
        region = conf['AWS_REGION']

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    tags = UnicodeAttribute(null=True)
    desc = UnicodeAttribute(null=True)
    filename_orig = UnicodeAttribute(null=True)
    filename = UnicodeAttribute(null=True)
    filesize = NumberAttribute(null=True)
    geotag_lat = UnicodeAttribute(null=True)
    geotag_lng = UnicodeAttribute(null=True)
    upload_date = UTCDateTimeAttribute(default=datetime.now(get_localzone()))
    taken_date = UTCDateTimeAttribute(null=True)
    make = UnicodeAttribute(null=True)
    model = UnicodeAttribute(null=True)
    width = UnicodeAttribute(null=True)
    height = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    nation = UnicodeAttribute(null=True)
    address = UnicodeAttribute(null=True)


def create_photo_info(user_id, filename, filesize, form):
    new_photo = Photo(user_id=user_id,
                      id=filename,
                      filename=filename,
                      filename_orig=form['filename_orig'][0].decode('utf-8'),
                      filesize=filesize,
                      upload_date=datetime.today(),
                      tags=form['tags'][0].decode('utf-8'),
                      desc=form['desc'][0].decode('utf-8'),
                      geotag_lat=form['geotag_lat'][0].decode('utf-8'),
                      geotag_lng=form['geotag_lng'][0].decode('utf-8'),
                      taken_date=datetime.strptime(form['taken_date'][0].decode('utf-8'), "%Y:%m:%d %H:%M:%S"),
                      make=form['make'][0].decode('utf-8'),
                      model=form['model'][0].decode('utf-8'),
                      width=form['width'][0].decode('utf-8'),
                      height=form['height'][0].decode('utf-8'),
                      city=form['city'][0].decode('utf-8'),
                      nation=form['nation'][0].decode('utf-8'),
                      address=form['address'][0].decode('utf-8'))
    return new_photo


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'attribute_values'):
            return obj.attribute_values
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


if not Photo.exists():
    Photo.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB Photo table created!')


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
