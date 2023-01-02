from datetime import timedelta
from flask import Blueprint, render_template, request, url_for, redirect, flash, g, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
#auth.permanent_session_lifetime = timedelta(minutes = 1)

@auth.before_request
def before_request():
    session.permanent = True
    permanent_session_lifetime = timedelta(minutes=1)
    session.modified = True
    g.user = current_user
    '''
    session_permanent = True
    auth.permanent_session_lifetime = timedelta(minutes=1)
    session_modified = True
    g.user = current_user
    #login_user(current_user, remember=False)
    '''


@auth.route('/sign-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/start', methods =["POST", "GET"])
def startAccount():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        isPWUpper = any(letter.isupper() for letter in password1)

        user = User.query.filter_by(firstName = fname).first()
        if user:
            flash("username already taken", category = "error")
        elif len(fname) < 2:
            flash("first name must be greater than 1 characters", category= "error")
        elif len(lname) < 2:
            flash("last name must be greater than 1 characters", category= "error")
        elif len(username) < 3:
            flash("username must be longer than 2 characters", category="error")
        elif len(password1) < 6:
            flash("password must be greater than 5 characters", category= "error")
        elif not isPWUpper:
            flash("password must have a capital letter", category="error") 
        elif password1 != password2:
            flash("passwords don't equal each other", category= "error")
        else: 
            newUser = User(email=email, firstName=fname, password=generate_password_hash(
                password1, method='sha256'), balance = 0.00)
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser)
            #did this different

            flash("Account created", category="success")
            return redirect(url_for('views.home'))
    return render_template("startaccount.html", user = current_user)



@auth.route('/sign-in', methods =["POST", "GET"])
def login():
    if request.method == "POST":
        #session_permanent = True
        #auth.permanent_session_lifetime = timedelta(minutes = 1)
        #auth.session.modified = True
        fname = request.form.get('fname')
        password = request.form.get('password')
        user = User.query.filter_by(firstName = fname).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember= True)

                flash("Logged in successfull!", category = "success")
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password, try again", category = "error")

        else:
            flash("No account exists with that username", category="error")
    return render_template("signin.html", user = current_user)


@auth.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

