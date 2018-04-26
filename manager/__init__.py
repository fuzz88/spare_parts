# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from manager.models import SparePartsManager

app = Flask(__name__)


@app.route('/')
def index():
    manager = SparePartsManager()
    return jsonify(manager._parts)
