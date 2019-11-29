# auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.model.user_model import User
from app import db

user = Blueprint('user', __name__)

@user.route('/user/list')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user/user_list.html', users=users, title="User List")


@user.route('/user/add')
@login_required
def user_add():
    user=User()
    return render_template('user/user_form.html',user=user,title="User Add")

@user.route('/user/edit/<int:id>')
@login_required
def user_edit(id):
    user = User.query.get_or_404(id)
    return render_template('user/user_form.html',user=user,title="User Edit")  

@user.route('/user/delete/<int:id>')
@login_required
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.user_list'))  



@user.route('/user/save', methods=['POST'])
@login_required
def user_save():
    form_user=User()
    form_user.id = request.form.get('id')
    form_user.first_name = request.form.get('first_name')
    form_user.last_name = request.form.get('last_name')
    form_user.email = request.form.get('email')
    form_user.is_admin = request.form.get('is_admin')
    
    exist_user = User.query.filter_by(email=form_user.email).first()
    
    if(User.isSuperAdmin(form_user.email)):
        flash('Email address already exists')
        return redirect(url_for('user.user_edit',id=form_user.id))
        
    if(form_user.id is not None and form_user.id>0):
        user= User.query.get_or_404(form_user.id)
        if(exist_user and  exist_user.id!=form_user.id):
            flash('Email address already exists')
            return redirect(url_for('user.user_edit',id=form_user.id))
        user.first_name=form_user.first_name
        user.last_name=form_user.last_name
        user.email=form_user.email
        db.session.add(user)
        db.session.commit()
    else:
        if(exist_user):
            flash('Email address already exists')
            return redirect(url_for('auth.user_add'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if(password != confirm_password):
            flash('Password and confirm password are not same')
            return redirect(url_for('user.user_add'))
        form_user.password=generate_password_hash(password, method='sha256')
        db.session.add(form_user)
        db.session.commit()

    return redirect(url_for('user.user_edit',id=form_user.id))      
