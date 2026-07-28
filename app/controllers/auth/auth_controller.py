
from datetime import time
from functools import wraps
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app import flask_bcrypt

from app.model.user import UserRepository

auth = Blueprint('auth', __name__)

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session or session['user_id'] is None:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def update_session(user_id):
    """Update the session with user details."""
    if user_id:
        user = UserRepository.get_user(user_id = user_id)
        session['loggedin'] = True
        session['user_id'] = user['user_id']
        session['username'] = user['username']

# This is a helper function to decide where the user should go
def get_user_destination():
    
    if 'loggedin' in session:
        return url_for('user.dashboard')
    else:
        return url_for('auth.home')

@auth.route('/')
def root():

    return redirect(get_user_destination())

@auth.route('/home')
def home():
    
    if 'loggedin' in session:
        return redirect(url_for('user.dashboard'))
    
    return render_template('home.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    # if 'loggedin' in session:
    #     return redirect(get_user_destination())

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        session.permanent = True
        username = request.form['username']
        password = request.form['password']
        
        # Attempt to validate the login details against the database.
        account = UserRepository.get_user(username=username)

        if account is not None:
            password_hash = account['password_hash']

            if flask_bcrypt.check_password_hash(password_hash, password):
                update_session(user_id = account['user_id'])
                return redirect(get_user_destination())
            else:
                flash('Username or password is wrong', 'error')
                return render_template('auth/login.html',
                                       username=username,
                                       invalid_login=True)
        else:
            flash('Username or password is wrong', 'error')
            return render_template('auth/login.html',
                                   username=username,
                                   invalid_login=True)
    
    elif 'username' in session:
        
        return redirect(url_for('user.dashboard'))
    
    
    return render_template('auth/login.html')



@auth.route('/logout')
def logout():
    # removes session data when logged out
    session.clear()
    return redirect(url_for('auth.home'))
