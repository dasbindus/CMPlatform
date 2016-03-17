#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'


from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response, jsonify
from . import api
from .. import db
from ..models import Permission, User, Role
from ..decorators import admin_required, permission_required


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

