import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from core.db import create_conn
from core.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cnx, cursor = create_conn()
        error = None

        #validate form
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'

        #cereate user
        if error is None:
            try:
                user = User(username, password, email)
                user.create_user(cursor)
                cnx.close()
            except Exception as e:
                print(e)
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cnx, cursor = create_conn()
        error = None
        #create object User
        user = User(username, password)

        #check user
        if not user.check_user(cursor):
            error = 'Incorrect password or username.'
        if error is None:
            #clear session and put user in session
            session.clear()
            session['user_id'] = User.load_user_by_username(cursor, username).id
            cnx.close()
            return redirect(url_for('index'))
        cnx.close()
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cnx, cursor = create_conn()
        g.user = User.get_user_by_id(cursor, user_id)
        cnx.close()

#decorator for redirect to login view
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #if user is not login
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view