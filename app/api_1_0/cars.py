from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from . import api
from ..models import User, Car, Permission
from .errors import not_found, forbidden
from .decorators import permission_required
import datetime


__author__ = 'Jack'


@api.route('/cars/', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    return jsonify({
        'cars': [car.to_json() for car in cars],
        'count': len(cars),
        'time': datetime.datetime.utcnow()
    })


@api.route('/cars/', methods=['POST'])
@permission_required(Permission.ADMINISTER)
def new_car():
    car = Car.from_json(request.json)
    car.owner = g.current_user
    db.session.add(car)
    db.session.commit()
    return jsonify({
        'car': car.to_json(),
        'create_at': datetime.datetime.utcnow()
    }), 201, {'Location': url_for('api.get_car', id=car.id, _external=True)}


@api.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    car = Car.query.get(id)
    if car is not None:
        return jsonify(car.to_json())
    else:
        return not_found('resources not found.')


@api.route('/cars/<int:id>', methods=['DELETE'])
@permission_required(Permission.ADMINISTER)
def delete_car(id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'delete car successfully.'})
    else:
        return not_found('recources not found')



