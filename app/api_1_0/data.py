#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'


from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response, jsonify
from . import api
from .errors import forbidden, bad_request, unauthorized, not_found
from .. import db
from ..models import Permission, User, Post, Car, CarData
from ..emails import send_email
from .decorators import permission_required
import datetime






@api.route('/data/<int:id>', methods=['GET'])
def get_data(id):
    data = CarData.query.get_or_404(id)
    return jsonify(data.to_json())

