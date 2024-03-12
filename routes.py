from flask import Flask, render_template, request, session, url_for, redirect, make_response
from models import User
from imports import db, mail, app
from flask_mail import Message


@app.route('/mail', methods=['GET'])
def mail_1():
    msg = Message(
        subject='Registration letter',
        sender='noreply@employer.com',
        recipients=['wfe@wef.wef']
    )
    msg.html = 'wef'
    mail.send(msg)


@app.route('/')
def index():
    return str(session.get('user_id', 'Please, you must login !!!'))


@app.route('/register', methods=['POST'])
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

        return 'no problem'

    return render_template('register.html')


@app.route('/login', methods=['POST'])
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


