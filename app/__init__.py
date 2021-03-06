#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    '''
    create_app() 函数就是程序的工厂函数,接受一个参数,是程序使用的配置名。
    配置类在 config.py 文件中定义,其中保存的配置可以使用 Flask app.config 
    配置对象提供的 from_object() 方法直接导入程序。至于配置对象,则可以通过
    名字从 config 字典中选择。
    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # ============注册BluePrint===================

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    
    return app
