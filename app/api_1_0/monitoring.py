from flask import url_for, current_app, request, jsonify
from . import api
from .errors import forbidden, bad_request, unauthorized, not_found
from .. import db
from ..models import Permission, User, Role, Post, Car
import datetime
import subprocess


__author__ = 'Jack Bai'



@api.route('/heartbeat', methods=['GET'])
def heartbeat():
    version = current_app.config['VERSION']
    return jsonify({
        'version': version,
        'status': 'OK',
        'status_code': 777,
        'time': datetime.datetime.utcnow()
    })


@api.route('/diagnostic', methods=['GET'])
def diagnostic():
    is_db_working = False
    is_db_connected = False
    # check if working
    p = subprocess.Popen("netstat -ant | grep 3306 | grep LISTEN", stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    if out != '' and err is None:
        is_db_working = True
    else:
        db_status = 'Can not find mysql process.'
        status_code = 2
    # check if connected
    try:
        results = db.session.execute("SELECT VERSION()")
        if results:
            is_db_connected = True
        else:
            db_status = 'Can not connected to mysql.'
            status_code = 3
    except MySQLdb.Error, e:
        err_message =  "ERROR %d IN CONNECTION: %s" % (e.args[0], e.args[1])
    if is_db_working and is_db_connected:
        db_status = 'OK'
        status_code = 1
        err_message = None
    return jsonify({
        'database status': db_status,
        'status_code': status_code,
        'err_message': err_message,
        'time': datetime.datetime.utcnow()
    })

