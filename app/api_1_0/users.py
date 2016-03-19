#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'


from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response, jsonify
from . import api
from .errors import forbidden, bad_request, unauthorized
from .. import db
from ..models import Permission, User, Role
from ..decorators import admin_required, permission_required
import datetime
# import json




@api.route('/users/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify({
        'user': [user.to_json() for user in users],
        'count': len(users),
        'time': datetime.datetime.utcnow() 
    })


@api.route('/users/', methods=['POST'])
# @permission_required(Permission.) # TODO Permission Design
def new_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({user.to_json()}), 201


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>', methods=['DELETE'])
# @permission_required
def delete_user(id):
    pass


@api.route('/users/<int:id>/posts/', methods=['GET'])
def get_user_posts(id):
    # TODO Add relatoinship between User and Post

    # user = User.query.get_or_404(id)
    # page = request.args.get('page', 1, type=int)
    # pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    # posts = pagination.items
    # prev = None
    # next=None
    # if pagination.has_prev:
    #     prev = url_for('', page=page-1, _external=True)
    # if pagination.has_next:
    #     next = url_for('', page=page+1, _external=True)
    # return jsonify({
    #     'posts': [post.to_json() for post in posts],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total,
    #     'time': datetime.datetime.utcnow()
    # })
    pass


@api.route('/users/<int:id>/cars/', methods=['GET'])
def get_user_cars(id):
    # user = User.get_or_404(id)
    # page = request.args.get('page', 1, type=int)
    # pagination = user.cars.order_by(Car.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['CARS_PER_PAGE'], error_out=False)
    # cars = pagination.items
    # prev = None
    # next = None
    # if pagination.has_prev:
    #     prev = url_for('', page=page-1, _external=True)
    # if pagination.has_next:
    #     next = url_for('', page=page+1, _external=True)
    # return jsonify({
    #     'cars': [car.to_json() for car in cars],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total,
    #     'time': datetime.datetime.utcnow()
    # })
    pass
