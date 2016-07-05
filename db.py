#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import g
import sqlite3

def connect_db(database_path):
    rv = sqlite3.connect(database_path)
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()