from flask import Flask, render_template, g, request, flash, url_for, redirect, session
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

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


########################## View functions ##################3

@app.route('/')
def show_tree():
    if session.get('logged_in'):
        db = get_db()
        query = '''select *
                from person
                where id = ?
                '''
        cur = db.execute(query, [session['user_id']])
        people = cur.fetchall()

        return render_template('show_tree.html', people=people)
    else:
        return render_template('show_tree.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username_r']
        password = request.form['password_r']

        db = get_db()
        query = '''select *
                from users
                where username = ?'''
        cur = db.execute(query, [username])
        result = cur.fetchone()

        if result is None:
            error = "Ta nazwa uzytkownika jest juz zajeta"
        else:
            query = '''insert into users (username, password)
                    values (?, ?)'''
            db.execute(query, [username, password])
            db.commit()

            query = '''select id
                    from users
                    where username = ?'''
            cur = db.execute(query, [username])
            user_id = cur.fetchone()[0]
            session['logged_in'] = True
            session['user_id'] = user_id
            session['username'] = username
            flash('Utworzono nowe konto')
            return redirect(url_for('show_tree'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username_l']
        password = request.form['password_l']

        db = get_db()
        query = '''select id, password
                from user
                where username = ?'''
        cur = db.execute(query, [username])
        result = cur.fetchone()

        if result is None:
            error = "Nie ma takiego uzytkownika"
        else:
            pwd = result[1]
            if password != pwd:
                error = "Haslo jest nieprawidlowe"
            else:
                session['logged_in'] = True
                session['user_id'] = result[0]
                session['username'] = username
                flash('Jestes zalogowany')
                return redirect(url_for('show_tree'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('username', None)
        flash('Zostales wylogowany')
    return redirect(url_for('show_tree'))

@app.route('/add')
def add_new_person():
    return "nowa osoba"

if __name__ == "__main__":
    app.run()