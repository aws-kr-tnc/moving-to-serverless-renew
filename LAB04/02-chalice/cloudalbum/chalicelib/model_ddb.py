from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection
from datetime import datetime
from tzlocal import get_localzone
from chalicelib.config import conf
import json


def local_time_now():
    local_tz = get_localzone()
    return datetime.now(local_tz)


def photo_deserialize(photo):
    photo_json = {}
    photo_json['user_id'] = photo.user_id
    photo_json['id'] = photo.id
    photo_json['filename'] = photo.filename
    photo_json['filename_orig'] = photo.filename_orig
    photo_json['filesize'] = photo.filesize
    photo_json['upload_date'] = photo.upload_date
    photo_json['tags'] = photo.tags
    photo_json['desc'] = photo.desc
    photo_json['geotag_lat'] = photo.geotag_lat
    photo_json['geotag_lng'] = photo.geotag_lng
    photo_json['taken_date'] = photo.taken_date
    photo_json['make'] = photo.make
    photo_json['model'] = photo.model
    photo_json['width'] = photo.width
    photo_json['height'] = photo.height
    photo_json['city'] = photo.city
    photo_json['nation'] = photo.nation
    photo_json['address'] = photo.address
    return photo_json


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
