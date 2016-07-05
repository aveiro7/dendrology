#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
from db import connect_db

def set_mail_config(app, db):
    query = '''select value
            from config
            where key = ?'''
    mail_server = db.execute(query, ["mail_server"]).fetchone()[0]
    mail_username = db.execute(query, ["mail_username"]).fetchone()[0]
    mail_password = db.execute(query, ["mail_password"]).fetchone()[0]
    
    app.config.update(dict(
        MAIL_SERVER=mail_server,
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password
        ))

def set_cookie_config(app, db):
    query = '''select value
            from config
            where key = ?'''
    secret_key = db.execute(query, ["secret_key"]).fetchone()[0]

    app.config['SECRET_KEY'] = secret_key

def set_config(app):
    db = connect_db(app.config['DATABASE'])

    set_cookie_config(app, db)
    set_mail_config(app, db)
    db.close()