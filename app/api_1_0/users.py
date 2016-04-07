#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'


from flask import render_template, abort, session, redirect, url_for, \
    current_app, flash, request, make_response, jsonify
from . import api
from .errors import forbidden, bad_request, unauthorized
from .. import db
from ..models import Permission, User, Role, Post, Car
from ..emails import send_email
from .decorators import permission_required
from .errors import not_found
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
@permission_required(Permission.ADMINISTER)
def new_user():
    user = User.from_json(request.json)
    token = user.generate_confirmation_token()
    send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'user': user.to_json(),
        'create_at': datetime.datetime.utcnow()
    }), 201, {'Location': url_for('api.get_user', id=user.id, _external=True)}


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is not None:
        return jsonify(user.to_json())
    else:
        return not_found('resources not found.')


@api.route('/users/<int:id>', methods=['DELETE'])
@permission_required(Permission.ADMINISTER)
def delete_user(id):
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'delete successfully.'})
    else:
        return not_found('resources not found.')


@api.route('/users/<int:id>/posts/', methods=['GET'])
def get_user_posts(id):
    user = User.query.get(id)
    if user is None:
        return not_found('resources not found.')
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    next=None
    if pagination.has_prev:
        prev = url_for('', page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'time': datetime.datetime.utcnow()
    })



@api.route('/users/<int:id>/cars/', methods=['GET'])
def get_user_cars(id):
    user = User.query.get(id)
    if user is None:
        return not_found('resources not found.')
    page = request.args.get('page', 1, type=int)
    pagination = user.cars.order_by(Car.register_since.desc()).paginate(
        page, per_page=current_app.config['CARS_PER_PAGE'], error_out=False)
    cars = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('', page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('', page=page+1, _external=True)
    return jsonify({
        'cars': [car.to_json() for car in cars],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'time': datetime.datetime.utcnow()
    })

