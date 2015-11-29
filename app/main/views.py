#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response
from flask.ext.login import login_required
from .. import db
from . import main
from ..models import User, Role
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)



@main.route('/test', methods=['GET', 'POST'])
def test_index():
    return render_template('test_index_01.html')




# [-----------------------------------------------]
# [             JQuery Mobile Tests               ]
# [-----------------------------------------------]
@main.route('/mobile/1', methods=['GET', 'POST'])
def jquery_mobile_test1():
    return render_template('mobile/test1.html')


@main.route('/mobile/2', methods=['GET', 'POST'])
def jquery_mobile_test2():
    return render_template('mobile/test2.html')
