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



@api.route('/data/', methods=['GET'])
def get_all_data():
    page = request.args.get('page', 1, type=int)
    pagination = CarData.query.paginate(
        page, per_page=current_app.config['DATA_PER_PAGE'], error_out=False)
    datas = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_all_data', page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('api.get_all_data', page=page+1, _external=True)
    return jsonify({
        'cars': [data.to_json() for data in datas],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'time': datetime.datetime.utcnow()
    })



@api.route('/data/<int:id>', methods=['GET'])
def get_data(id):
    data = CarData.query.get_or_404(id)
    return jsonify(data.to_json())


@api.route('/data/<int:id>', methods=['PUT'])
@permission_required(Permission.ADMINISTER)
def update_data(id):
    data_exist = CarData.query.get(id)
    # TODO throw forbidden when not owner or admin
    if data_exist is None:
        return not_found('Resources not found. Please POST to create.')
    data = CarData.from_json(request.json)
    data.car_id = id
    db.session.add(data)
    db.session.commit()
    return jsonify({
        'data': data.to_json(),
        'create_at': datetime.datetime.utcnow()
    })

