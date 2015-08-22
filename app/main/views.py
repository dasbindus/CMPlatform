#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, current_app, flash, request, make_response
from .. import db
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
