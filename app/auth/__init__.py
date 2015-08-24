#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
