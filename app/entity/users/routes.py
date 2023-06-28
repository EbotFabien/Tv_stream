from flask import render_template, url_for,flash,redirect,request,abort,Blueprint
from app.entity.users.forms import LoginForm,RegistrationForm,CreateForm
from app.Models import User,Suggestion,Journey
from flask_login import login_user,current_user,logout_user,login_required
from app import bcrypt,db
from datetime import date,timedelta,datetime,timezone 
import random
from sqlalchemy import or_, and_, desc,asc
from werkzeug.utils import secure_filename
from flask import  url_for,current_app
import os







users =Blueprint('users',__name__)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.Type=='admin':
            return redirect(url_for('users.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        name=User.query.filter_by(username=form.username.data).first()#put login
        if  name and bcrypt.check_password_hash(name.password,form.password.data):
            login_user(name,remember=form.remember.data,duration=timedelta(seconds=30)) 
            next_page=request.args.get('next')
            return redirect (next_page) if next_page else  redirect(url_for('users.dashboard'))
        else:
    
            flash(f'Mauvais Identifiant ou mot de passe, essayez à nouveau','danger')

    return render_template('login.html',legend="login",form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/dashboard')
def dashboard():
    loc=User.query.filter_by(Type='Broadcaster').all()
    return render_template('dashboard.html',loc=loc)

@users.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if current_user.is_authenticated:
       return redirect(url_for('users.dashboard'))
    form = RegistrationForm()

    if form.validate_on_submit():#check user 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,Type=form.type.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created you can now login','success')
        return redirect(url_for('users.login'))
    return render_template('signup.html',legend="sign_up",form=form)

