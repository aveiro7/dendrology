#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, render_template, g, request, flash, url_for, redirect, session
import os
import sqlite3
from mail_sender import send_mail
from config import set_config
from . import app
from db import init_db, connect_db

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app.config['DATABASE'])
    return g.sqlite_db

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initialized the database."

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_tree():
    if session.get('logged_in'):
        db = get_db()
        query = '''select *
                from person
                where tree = ?
                '''
        people = db.execute(query, [session['user_id']]).fetchall()
    else:
        people = None

    return render_template('show_tree.html', people=people)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username_r']
        password = request.form['password_r']

        db = get_db()
        query = '''select *
                from user
                where username = ?'''
        cur = db.execute(query, [username])
        result = cur.fetchone()

        if result:
            error = "Ta nazwa użytkownika jest już zajęta"
            return render_template('register.html', error=error)
        
        query = '''insert into user (username, password)
                values (?, ?)'''
        db.execute(query, [username, password])
        db.commit()

        query = '''select id
                from user
                where username = ?'''
        cur = db.execute(query, [username])
        user_id = cur.fetchone()[0]
        session['logged_in'] = True
        session['user_id'] = user_id
        session['username'] = username
        flash('Utworzono nowe konto')
        return redirect(url_for('show_tree'))

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username_l']
        password = request.form['password_l']

        db = get_db()
        query = '''select id, password
                from user
                where username = ?'''
        result = db.execute(query, [username]).fetchone()
        
        if result is None:
            error = "Nie ma takiego użytkownika"
            return render_template('login.html', error=error)

        user_id, pwd = result

        if password != pwd:
            error = "Hasło jest nieprawidłowe"
            return render_template('login.html', error=error)

        session['logged_in'] = True
        session['user_id'] = user_id
        session['username'] = username
        flash(u'Jesteś zalogowany')
        return redirect(url_for('show_tree'))

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('username', None)
        flash(u'Zostałeś wylogowany')
    return redirect(url_for('show_tree'))

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    error = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']

        db = get_db()
        query = '''insert into person
                (first_name, last_name, birth_year, tree)
                values (?, ?, ?, ?)'''
        db.execute(query, [first_name, last_name, birth_date, session['user_id']])
        db.commit()
        flash(u'Osoba pomyślnie dodana')
        return redirect(url_for('show_tree'))

    else:
        db = get_db()
        query = '''select first_name, last_name
                from person
                '''
        cur = db.execute(query)
        people = cur.fetchall()
        return render_template('add_person.html', error=error, people=people)

@app.route('/edit_person/<person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    db = get_db()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']

        query = '''update person
                set first_name = ?,
                last_name = ?,
                birth_year = ?
                where id = ?'''

        db.execute(query, [first_name, last_name, birth_date, person_id])
        db.commit()
        flash("Zmieniono dane")
        return redirect(url_for('show_tree'))

    else:
        query = '''select *
                from person
                where id = ?
                '''
        cur = db.execute(query, [person_id])
        result = cur.fetchone()
        return render_template('edit_person.html', person=result)

@app.route('/delete_person/<person_id>')
def delete_person(person_id):
    db = get_db()
    query = '''delete from person
            where id = ?'''
    db.execute(query, [person_id])
    db.commit()
    flash(u"Usunięto wpis")
    return redirect(url_for('show_tree'))

@app.route('/send_email')
def send_email():
    send_mail(app, "", "asdf")
    flash(u"Wysłano wiadomość")
    return redirect(url_for('show_tree'))

if __name__ == "__main__":
    app.run()
