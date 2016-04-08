from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from . import api
from ..models import User, Car, Permission, CarData
from .errors import not_found, forbidden
from .decorators import permission_required
import datetime


__author__ = 'Jack'



@api.route('/cars/', methods=['GET'])
def get_all_cars():
    page = request.args.get('page', 1, type=int)
    pagination = Car.query.paginate(
        page, per_page=current_app.config['CARS_PER_PAGE'], error_out=False)
    cars = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_all_cars', page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('api.get_all_cars', page=page+1, _external=True)
    return jsonify({
        'cars': [car.to_json() for car in cars],
        'prev': prev,
        'next': next,
        'count': pagination.total,
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


@api.route('/cars/<int:id>/data/', methods=['GET'])
def get_car_data(id):
    page = request.args.get('page', 1, type=int)
    car = Car.query.get_or_404(id)
    pagination = car.data.order_by(CarData.timestamp.desc()).paginate(
        page, per_page=current_app.config['DATA_PER_PAGE'], error_out=False)
    data_all = pagination.items
    prev = None
    next = None
    if pagination.has_prev:
        prev = url_for('api.get_car_data', id=id, page=page-1, _external=True)
    if pagination.has_next:
        next = url_for('api.get_car_data', id=id, page=page+1, _external=True)
    return jsonify({
        'data': [data.to_json() for data in data_all],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'time': datetime.datetime.utcnow()
    })


@api.route('/cars/<int:id>/data/', methods=['POST'])
@permission_required(Permission.ADMINISTER)
def new_car_data(id):
    data = CarData.from_json(request.json)
    data.car_id = id
    db.session.add(data)
    db.session.commit()
    return jsonify({
        'data': data.to_json(),
        'create_at': datetime.datetime.utcnow()
    }), 201,\
    {'Location': url_for('api.get_data', id=data.id, _external=True)}
    


@api.route('/cars/<int:id>/data/<int:datetime>', methods=['GET'])
def get_car_data_date(id, datetime):
    pass


@api.route('/cars/<int:id>/data/<int:datetime>', methods=['DELETE'])
def delete_car_data_date(id, datetime):
    pass


QUERY_TYPE = {'': 1, '': 2, '': 3}


@api.route('/cars/<int:id>/data/query/', methods=['POST'])
def query_car_data(id):
    # json_request = request.json
    # query_type_id = json_request.get('')
    pass






