from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from . import api
from ..models import User, Car, Permission, CarData
from .errors import not_found, forbidden, bad_request
from .decorators import permission_required
import datetime
import json
import decimal


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


QUERY_TYPE = {'OBD': 1, 'ENV': 2, 'LOCATION': 3, 'VIDEO': 4, 'ALL': 5}
OBD_DATA = ['obd_rpm', 'obd_vss', 'obd_ect', 'obd_maf', 'obd_map', 'obd_o1v']
ENV_DATA = ['env_temperature', 'env_humidity', 'env_pm25']

def decimal2float(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif obj is None:
        return None
    raise TypeError


@api.route('/cars/<int:id>/data/query/', methods=['POST'])
def query_car_data(id):
    car = Car.query.get_or_404(id)
    json_request = request.json
    query_id = json_request.get('query_id')
    query_at = json_request.get('query_at')
    query_paras = json_request.get('query_paras')
    if query_id is None:
        return bad_request('Bad query request.')
    nowtime = datetime.datetime.utcnow()
    # TODO 0 <= (nowtime - query_at) <= 1 hour
    if query_paras is None:
        return bad_request('No query parameters.')
    query_type_id = query_paras.get('query_type_id')
    range_start = query_paras.get('range_start')
    range_end = query_paras.get('range_end')
    data_per_page = query_paras.get('data_per_page')
    if data_per_page is None:
        data_per_page = 100
    # Check if query_paras meet the requirements
    para_list = [query_type_id, range_start, range_end, data_per_page]
    for para in para_list:
        if para:
            continue
        else:
            return bad_request('Parameters is illegal.')
    page = request.args.get('page', 1, type=int)
    # the order of query parameters CAN'T change.
    if query_type_id == QUERY_TYPE['OBD']:
        pagination = CarData.query.with_entities(CarData.obd_rpm, CarData.obd_vss,
            CarData.obd_ect, CarData.obd_maf, CarData.obd_map, CarData.obd_o1v).filter(
            CarData.timestamp.between(range_start, range_end)).paginate(
            page, per_page=data_per_page, error_out=False)
        datas = pagination.items
        prev = None
        next = None
        if pagination.has_prev:
            prev = url_for('api.query_car_data', id=id, page=page-1, _external=True)
        if pagination.has_next:
            next = url_for('api.query_car_data', id=id, page=page+1, _external=True)
        return jsonify({
            'response_id': query_id,
            'data': json.dumps([dict(zip(data.keys(), [decimal2float(value) for value in data])) for data in datas]),
            'count': pagination.total,
            'prev': prev,
            'next': next,
            'response_time': datetime.datetime.utcnow()
        }), 201
    if query_type_id == QUERY_TYPE['ENV']:
        pagination = CarData.query.with_entities(CarData.env_temperature,
            CarData.env_humidity, CarData.env_pm25).filter(
            CarData.timestamp.between(range_start, range_end)).paginate(
            page, per_page=data_per_page, error_out=False)
        datas = pagination.items
        prev = None
        next = None
        if pagination.has_prev:
            prev = url_for('api.query_car_data', id=id, page=page-1, _external=True)
        if pagination.has_next:
            next = url_for('api.query_car_data', id=id, page=page+1, _external=True)
        return jsonify({
            'response_id': query_id,
            'data': json.dumps([dict(zip(data.keys(), [decimal2float(value) for value in data])) for data in datas]),
            'count': pagination.total,
            'prev': prev,
            'next': next,
            'response_time': datetime.datetime.utcnow()
        }), 201
    if query_type_id == QUERY_TYPE['VIDEO']:
        pagination = CarData.query.with_entities(
            CarData.video_path).filter(
            CarData.timestamp.between(range_start, range_end)).paginate(
            page, per_page=data_per_page, error_out=False)
        datas = pagination.items
        prev = None
        next = None
        if pagination.has_prev:
            prev = url_for('api.query_car_data', id=id, page=page-1, _external=True)
        if pagination.has_next:
            next = url_for('api.query_car_data', id=id, page=page+1, _external=True)
        return jsonify({
            'response_id': query_id,
            'data': json.dumps([dict(zip(data.keys(), [decimal2float(value) for value in data])) for data in datas]),
            'count': pagination.total,
            'prev': prev,
            'next': next,
            'response_time': datetime.datetime.utcnow()
        }), 201
    return bad_request('Unknown query type.')







