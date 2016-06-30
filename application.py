from flask import Flask, render_template, g
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'trees.db'),
    SECRET_KEY='development_key'
))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initialized the database."

# this would be called every time the app context tears down
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_tree():
    return render_template('show_tree.html')

@app.route('/register')
def register():
    return "register"

@app.route('/login')
def login():
    return "login"

@app.route('/logout')
def logout():
    return "logout"

if __name__ == "__main__":
    app.run()