#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask
import os
from config import set_config


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'trees.db')

set_config(app)