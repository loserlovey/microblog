from datetime import datetime
from flask import render_template, flash, redirect, g, session, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from . import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User

@app.route('/index')
@app.route('/')
@login_required
def index():
    title= 'Welcome'
    user = g.user

    posts = [
        {
            'author': {'nickname': 'Jack'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Marry'},
            'body': 'The Avengers movie was so cool!'         
        }
    ]
    return render_template('index.html',title=title,name=user,post=posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        return oid.try_login(loginForm.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', form = loginForm, providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'post #1'},
        {'author': user, 'body': 'post #2'}
    ]
    return render_template("user.html", user = user, posts=posts)


@app.route('/edit', methods = ['POST', 'GET'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form = form)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
