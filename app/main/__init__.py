#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from flask import Blueprint

main = Blueprint('main', __name__)

# 末尾导入views & errors, 这是为了避免循环导入依赖, 因为在views.py 和 errors.py 中还要导入蓝本 main
from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
