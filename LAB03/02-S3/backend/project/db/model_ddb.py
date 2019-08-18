from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection

from tzlocal import get_localzone

from project.util.config import conf

def local_time_now():
    local_tz = get_localzone()
    return datetime.now(local_tz)

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


class Photo(MapAttribute):
    id= UnicodeAttribute(null=False)
    filename = UnicodeAttribute(null=False)
    filename_orig = UnicodeAttribute(null=False)
    filesize = NumberAttribute(null=False)
    upload_date = UTCDateTimeAttribute(default=local_time_now())

    tags = UnicodeAttribute(null=True)
    desc = UnicodeAttribute(null=True)
    geotag_lat = UnicodeAttribute(null=True)
    geotag_lng = UnicodeAttribute(null=True)
    taken_date = UTCDateTimeAttribute(default=local_time_now())
    make = UnicodeAttribute(null=True)
    model = UnicodeAttribute(null=True)
    width = UnicodeAttribute(null=True)
    height = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    nation = UnicodeAttribute(null=True)
    address = UnicodeAttribute(null=True)


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
    photos = ListAttribute(of=Photo, null=True)

    # def __iter__(self):
    #     for name, attr in self.get_attributes().items():
    #         if isinstance(attr, MapAttribute):
    #             if getattr(self, name):
    #                 yield name, getattr(self, name).as_dict()
    #         elif isinstance(attr, UTCDateTimeAttribute):
    #             if getattr(self, name):
    #                 yield name, attr.serialize(getattr(self, name))
    #         elif isinstance(attr, NumberAttribute):
    #             # if numeric return value as is.
    #             yield name, getattr(self, name)
    #         else:
    #             yield name, attr.serialize(getattr(self, name))
