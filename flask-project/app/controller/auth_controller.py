# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from app.model.user_model import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))        


@auth.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    
    if (not user and User.isSuperAdmin(email)):
        user=User.getSuperAdmin()
    
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    return redirect(url_for('home.index'))




