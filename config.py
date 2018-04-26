# -*- coding: utf-8 -*-
import os
import crayons

_basedir = os.path.abspath(os.path.dirname(__file__))

try:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
except KeyError:
    SECRET_KEY = 'Default FLASK_SECRET_KEY [1qaz2wsx3edczaq1xsw2cde3]'
    print(crayons.red(
          'WARNING: FLASK_SECRET_KEY that you are using now is NOT SAFE.\n'
          'You should setup your own FLASK_SECRET_KEY environment variable.'))

del os
del crayons
