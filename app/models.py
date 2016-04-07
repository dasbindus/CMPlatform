#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

"""
"""


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bleach
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager
import re
import decimal


def decimal2float(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError



# TODO
class Permission:
    """
    (not finished yet)
    """
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # TODO
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Brand(db.Model):
    """
    """
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    cars = db.relationship('Car', backref='brand', lazy='dynamic')

    def __repr__(self):
        return '<Brand %r>' % self.name



class PostType(db.Model):
    """
    """
    __tablename__ = 'post_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    posts = db.relationship('Post', backref='posttype', lazy='dynamic')

    def __repr__(self):
        return '<PostType %r>' % self.name




class Follow(db.Model):
    """
    """
    __tablename__ = 'follows'
    shop_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)




class Car(db.Model):
    """
    """
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.String(64), unique=True)
    register_since = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    data = db.relationship('CarData', backref='car', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

    def to_json(self):
        json_car = {
            'id': self.id,
            'license_number': self.license_number,
            'register_since': self.register_since,
            'owner': self.owner.name,
            'brand': self.brand.name
        }
        return json_car

    @staticmethod
    def from_json(json_car):
        license_number = json_car.get('license_number')
        brand_id = json_car.get('brand_id')
        if not license_number:
            raise ValidationError('license_number can not be empty.')
        if not brand_id:
            raise ValidationError('brand_id can not be empty.')
        car = Car.query.filter_by(license_number=license_number).first()
        if car:
            raise ValidationError('license_number already in use.')
        return Car(license_number=license_number, brand_id=brand_id)

    def __repr__(self):
        return '<Car %r>' % self.license_number



class CarData(db.Model):
    """
    """
    __tablename__ = 'car_data'
    id = db.Column(db.Integer, primary_key=True)
    obd_rpm = db.Column(db.DECIMAL(8,2))
    obd_vss = db.Column(db.DECIMAL(8,2))
    obd_ect = db.Column(db.DECIMAL(8,2))
    obd_maf = db.Column(db.DECIMAL(8,2))
    obd_map = db.Column(db.DECIMAL(8,2))
    obd_o1v = db.Column(db.DECIMAL(8,2))
    env_temperature = db.Column(db.DECIMAL(8,2))
    env_humidity = db.Column(db.DECIMAL(8,2))
    env_pm25 = db.Column(db.DECIMAL(8,2))
    video_path = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime())
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

    def __init__(self, **kwargs):
        super(CarData, self).__init__(**kwargs)

    def to_json(self):
        json_cardata = {
            'id': self.id,
            'obd_rpm': decimal2float(self.obd_rpm),
            'obd_vss': decimal2float(self.obd_vss),
            'obd_ect': decimal2float(self.obd_ect),
            'obd_maf': decimal2float(self.obd_maf),
            'obd_map': decimal2float(self.obd_map),
            'obd_o1v': decimal2float(self.obd_o1v),
            'env_temperature': decimal2float(self.env_temperature),
            'env_humidity': decimal2float(self.env_humidity),
            'env_pm25': decimal2float(self.env_pm25),
            'video_path': self.video_path,
            'timestamp': self.timestamp,
            'car_id': self.car_id
        }
        return json_cardata

    @staticmethod
    def from_json(json_cardata):
        obd_rpm = json_cardata.get('obd_rpm')
        obd_vss = json_cardata.get('obd_vss')
        obd_ect = json_cardata.get('obd_ect')
        obd_maf = json_cardata.get('obd_maf')
        obd_map = json_cardata.get('obd_map')
        obd_o1v = json_cardata.get('obd_o1v')
        env_temperature = json_cardata.get('env_temperature')
        env_humidity = json_cardata.get('env_humidity')
        env_pm25 = json_cardata.get('env_pm25')
        video_path = json_cardata.get('video_path')
        timestamp = json_cardata.get('timestamp')
        car_id = json_cardata.get('car_id')
        return CarData(obd_rpm=obd_rpm, obd_vss=obd_vss,\
            obd_ect=obd_ect, obd_maf=obd_maf, obd_map=obd_map, \
            obd_o1v=obd_o1v, env_temperature=env_temperature,\
            env_humidity=env_humidity, env_pm25=env_pm25,\
            video_path=video_path, timestamp=timestamp, car_id=car_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # ===== persional profile data =====
    name = db.Column(db.String(64))
    sex = db.Column(db.Boolean, default=True, index=True)
    age = db.Column(db.Integer) # change with year, seen by user only
    profession = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.TEXT())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    # ===== 4S Shop need more field ======
    # shop_name
    # phone_number
    # shop_confirmed
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    cars = db.relationship('Car', backref='owner', lazy='dynamic')
    drivers = db.relationship('Follow',
                                    foreign_keys=[Follow.shop_id],
                                    backref=db.backref('shop', lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')
    shops = db.relationship('Follow',
                                    foreign_keys=[Follow.driver_id],
                                    backref=db.backref('driver', lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')


    def __init__(self, **kw):
        super(User, self).__init__(**kw)
        if self.role is None:
            if self.email == current_app.config['MY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def drivers_cars(self):
        return Car.query.join(Follow, Follow.driver_id == Car.owner_id).filter_by(Follow.shop_id == self.id)

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'sex': self.sex,
            'age': self.age,
            'confirmation': self.confirmed,
            'member_since': self.member_since,
            'last_seen': self.last_seen
        }
        return json_user

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_shop(self):
        pass

    def is_driver(self):
        pass

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # only role is shop has permission to follow
    def follows(self, user):
        if not self.is_following(user):
            f = Follow(shop=self, driver=user)
            db.session.add(f)

    # only role is shop has permission to follow
    def unfollow(self, user):
        f = self.drivers.filter_by(driver_id=user.id).first()
        if f:
            db.session.delete(f)

    # for shop
    def is_following(self, user):
        return self.drivers.filter_by(driver_id=user.id).first() is not None

    # for driver(may never use)
    def is_followed_by(self, user):
        return self.shops.filter_by(shop_id=user.id).first() is not None

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    @staticmethod
    def from_json(json_user):
        email = json_user.get('email')
        username = json_user.get('username')
        password = json_user.get('password')
        _RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
        if not email or not _RE_EMAIL.match(email):
            raise ValidationError('email error.')
        if not username:
            raise ValidationError('username can not be empty.')
        if not password:
            raise ValidationError('password can not be empty.')
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('Email already in use.')
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError('Username already in use.')
        return User(email=email, 
                    username=username, 
                    password=password)

    def __repr__(self):
        return '<User %r>' % self.username



class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    """
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    summary = db.Column(db.Text)
    summary_html = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('post_type.id'))
    # TODO add relationship
    # comments=2abcfimos

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        attrs = {
            'img': ['src', 'alt'],
            'a': ['href']
        }
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        attrs = {
            'img': ['src', 'alt'],
            'a': ['href']
        }
        target.summary_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    def to_json(self):
        json_post = {
            'id': self.id,
            'author': self.author,
            'body': self.body,
            'body_html': self.body_html
        }
        return json_post

db.event.listen(Post.summary, 'set', Post.on_changed_summary)
db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    """
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # TODO add reply function

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)


