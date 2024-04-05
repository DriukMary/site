from flask import Flask, render_template, request, session, url_for, redirect, make_response
from models import User
from imports import db, mail, app
from flask_mail import Message
from werkzeug.utils import secure_filename
from flask import request


@app.route('/')
def index():
    return str(session.get('user_id', 'Please, you must login !!!'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return 'error: email already in use', 422

        user = User(username='123', email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        msg = Message(
            subject='Registration Confirmation',
            sender='noreply@employer.com',
            recipients=['wfe@wef.wef']
        )
        msg.html = 'Dear client {}, <br><br> Thank you for registering with us! Your registration was successful.'.format(
            email)
        mail.send(msg)

        return 'Registration successful. Confirmation email sent.'

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.is_password_correct(password):
            session['user_id'] = user.id
            if not request.cookies.get('username'):
                resp = make_response(user.username)
                resp.set_cookie('username', user.username, max_age=60)
            else:
                resp = make_response('Login successful')
            return resp

        return 'error: The information does not match', 422

    return render_template('login.html')


@app.route('/template')
def show_template():
    return render_template('index.html')
