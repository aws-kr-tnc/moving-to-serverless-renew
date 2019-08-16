from project import db
from sqlalchemy import Float, DateTime, ForeignKey, Integer, String
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """
    Database Model class for User table
    """
    __tablename__ = 'User'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(100), unique=True)
    username = db.Column(String(50), unique=False)
    password = db.Column(String(100), unique=False)

    photos = db.relationship('Photo',
                             backref='user',
                             cascade='all, delete, delete-orphan')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<%r %r %r>' % (self.__tablename__, self.username, self.email)

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }


class Photo(db.Model):
    """
    Database Model class for Photo table
    """
    __tablename__ = 'Photo'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(String(100), ForeignKey(User.id))
    tags = db.Column(String(400), unique=False)
    desc = db.Column(String(400), unique=False)
    filename_orig = db.Column(String(400), unique=False)
    filename = db.Column(String(400), unique=False)
    filesize = db.Column(Integer, unique=False)
    geotag_lat = db.Column(Float, unique=False)
    geotag_lng = db.Column(Float, unique=False)
    upload_date = db.Column(DateTime, unique=False)
    taken_date = db.Column(DateTime, unique=False)
    make = db.Column(String(400), unique=False)
    model = db.Column(String(400), unique=False)
    width = db.Column(String(400), unique=False)
    height = db.Column(String(400), unique=False)
    city = db.Column(String(400), unique=False)
    nation = db.Column(String(400), unique=False)
    address = db.Column(String(400), unique=False)

    def __init__(self, user_id, filename_orig, filename, filesize, upload_date, tags, desc, geotag_lat, geotag_lng,
                 taken_date, make, model, width, height):
        """Initialize"""

        self.user_id = user_id
        self.tags = tags
        self.desc = desc
        self.filename_orig = filename_orig
        self.filename = filename
        self.filesize = filesize
        self.geotag_lat = geotag_lat
        self.geotag_lng = geotag_lng
        self.upload_date = upload_date
        self.taken_date = taken_date
        self.make = make
        self.model = model
        self.width = width
        self.height = height
        # self.city = city
        # self.nation = nation
        # self.address = address

    def __repr__(self):
        """print information"""

        return '<%r %r %r>' % (self.__tablename__, self.user_id, self.upload_date)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tags': self.tags,
            'desc': self.desc,
            'filename_orig': self.filename_orig,
            'filename': self.filename,
            'filesize': self.filesize,
            'geotag_lat': self.geotag_lat,
            'geotag_lng': self.geotag_lng,
            'upload_date': self.upload_date,
            'taken_date': self.taken_date,
            'make': self.make,
            'model': self.model,
            'width': self.width,
            'height': self.height,
            'city': self.city,
            'nation': self.nation,
            'address': self.address
        }

    def insert_column(self, col, data):
        self[col] = data

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
