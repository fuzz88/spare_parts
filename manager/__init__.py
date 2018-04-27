# -*- coding: utf-8 -*-

from flask import Flask, render_template
from manager.models import SparePartsManager

app = Flask(__name__)

manager = SparePartsManager()


@app.route('/')
def index():
    return render_template('index.j2', parts=manager.parts_grouped)


@app.route('/order')
def order():
    return render_template('order.j2', parts=manager.parts_for_order)
