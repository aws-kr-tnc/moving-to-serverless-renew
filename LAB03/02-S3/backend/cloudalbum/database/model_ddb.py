from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection

from tzlocal import get_localzone

from cloudalbum.util.config import conf

def photo_deserialize(photo):
    photo_json = {}
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

class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'user-email-index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(['password'])

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    email = UnicodeAttribute(hash_key=True)


class User(Model):
    """
    User table for DynamoDB
    """

    class Meta:
        table_name = 'User'
        region = conf['AWS_REGION']

    id = UnicodeAttribute(hash_key=True)
    email_index = EmailIndex()
    email = UnicodeAttribute(null=False)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)


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