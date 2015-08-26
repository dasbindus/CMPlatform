#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

