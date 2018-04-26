# -*- coding: utf-8 -*-

from flask import Flask, render_template
from manager.models import SparePartsManager

app = Flask(__name__)


@app.route('/')
def index():
    manager = SparePartsManager()
    return render_template('test.j2', parts=manager._parts)
