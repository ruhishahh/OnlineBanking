from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Transaction, User
from . import db
from sqlalchemy import update

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", username = current_user.firstName, user = current_user, balance = current_user.balance) 


@views.route('/withdraw', methods =["POST", "GET"])
@login_required
def withdraw():
    if request.method == 'POST':
        transfer = request.form.get('transfer')

        change = User.query.filter_by(firstName=current_user.firstName).first()
        change.balance = current_user.balance - float(transfer)




        newTransaction = Transaction(transfer = transfer, user_id=current_user.id)
        db.session.add(newTransaction)
        db.session.commit()
        flash('Withdraw completed!', category='success')
        return render_template("home.html", username = current_user.firstName, balance = str(current_user.balance), user = current_user) 
    return render_template("withdraw.html", username = current_user.firstName, user = current_user)


@views.route("/deposit", methods =["POST", "GET"])
@login_required
def deposit():
    if request.method == 'POST':
        transfer = request.form.get('transfer')

        change = User.query.filter_by(firstName=current_user.firstName).first()
        change.balance = current_user.balance + float(transfer)

        newTransaction = Transaction(transfer = transfer, user_id=current_user.id, total = change.balance)
        db.session.add(newTransaction)
        db.session.commit()
        flash('Deposit completed!', category='success')
        return render_template("home.html", username = current_user.firstName, balance = str(current_user.balance), user = current_user)
    return render_template("deposit.html", username = current_user.firstName, user = current_user)






@views.route("/viewall")
def view():
    return render_template("viewall.html", user = current_user)
