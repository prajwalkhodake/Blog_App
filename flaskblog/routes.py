from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import app, db, bcrypt
from flask import Flask, flash, request
from flask import render_template, redirect
from flask import url_for
from flaskblog.forms import registrationFrom, loginFrom
from flaskblog.models import User, Post

posts = [
    {
        'author' : 'Corey Schfer',
        'title' : 'Blog Post 1',
        'content' : 'First post content',
        'date_posted' : 'March 18 , 2026'
    },
    {
        'author' : 'John Doe',
        'title' : 'Blog Post 2',
        'content' : 'Second post content',
        'date_posted' : 'March 19 , 2026'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registrationFrom()
    if form.validate_on_submit() :
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', tile= 'Register', form = form)
 
@app.route("/login", methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginFrom()
    if form.validate_on_submit() :
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html', tile= 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', tile= 'Account')