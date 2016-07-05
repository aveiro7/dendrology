import sqlite3

def set_config(app):

    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row

    query = '''select value
            from config
            where key = ?'''
    cur = db.execute(query, ["secret_key"])
    secret_key = cur.fetchone()[0]

    cur = db.execute(query, ["mail_server"])
    mail_server = cur.fetchone()[0]

    cur = db.execute(query, ["mail_username"])
    mail_username = cur.fetchone()[0]

    cur = db.execute(query, ["mail_password"])
    mail_password = cur.fetchone()[0]

    app.config.update(dict(
        SECRET_KEY=secret_key,
        MAIL_SERVER = mail_server,
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = mail_username,
        MAIL_PASSWORD = mail_password
        ))

