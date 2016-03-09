#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

import os
from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response
from flask.ext.login import login_required
from werkzeug import secure_filename
from .. import db
from . import main
from ..models import User, Role
from ..decorators import admin_required, permission_required


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    """
    Allowed upload file type.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    return render_template('portfolio.html')


@main.route('/services', methods=['GET', 'POST'])
def services():
    return render_template('services.html')


@main.route('/pricing', methods=['GET', 'POST'])
def pricing():
    return render_template('pricing.html')


@main.route('/founders', methods=['GET', 'POST'])
def founders():
    return render_template('founders.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

#[-------------------------------------------------]
#[                    profile                      ]
#[-------------------------------------------------]

@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def user_profile(username):
    app = current_app._get_current_object()
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'success'
        else:
            return 'upload file type is not supported.'
    return render_template('profile.html', user=user)


@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass


@main.route('/user/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    pass




# [-----------------------------------------------]
# [              Sample templates                 ]
# [-----------------------------------------------]
@main.route('/sample', methods=['GET', 'POST'])
def sample_index():
    return render_template('sample/index.html')


@main.route('/sample/test', methods=['GET', 'POST'])
def sample_index_test():
    return render_template('sample/test_index_01.html')




# [-----------------------------------------------]
# [             JQuery Mobile Tests               ]
# [-----------------------------------------------]
@main.route('/mobile/1', methods=['GET', 'POST'])
def jquery_mobile_test1():
    return render_template('mobile/test1.html')


@main.route('/mobile/2', methods=['GET', 'POST'])
def jquery_mobile_test2():
    return render_template('mobile/test2.html')
