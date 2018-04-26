#!/usr/bin/env python
# -*- coding: utf-8 -*-
from manager import app

app.config.from_object('config')
app.run(debug=True)
