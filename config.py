#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author_ = 'Jack Bai'

import os


class Config:
    """
    Basic configiration for Vehicle Monitor Platform.
    """
    SECRET_KEY = 'CaNYoUSeEMeNoW'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    VERSION = 'v1.0.0'

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[PLATFORM INFO]'
    MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    MY_ADMIN = os.environ.get('MY_ADMIN')

    POSTS_PER_PAGE = 2
    FOLLOWERS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 3
    USERS_PER_PAGE = 5
    CARS_PER_PAGE = 5
    DATA_PER_PAGE = 5

    UPLOAD_FOLDER = '/home/baidong/Uploads_test'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    '''
    configiration when developing.
    '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/car_server'


class TestingConfig(Config):
    '''
    configiration when testing.
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/car_server_test'


class ProductionConfig(Config):
    '''
    configiration when producting.
    '''
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/car_server'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
