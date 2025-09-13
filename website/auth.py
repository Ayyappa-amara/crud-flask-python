from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,logout_user,current_user,login_required, login_remembered
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method== "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in successfuly!..")
                # store logged-in details in login_user method. its predefind method from flask
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash("Incorrect password, Try again..", category="error")
        else:
            flash("Email not found.", category="error")
    return render_template("login.html", user= current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # check given email id is already existed in database
        user = User.query.filter(email=email).first()
        if user:
            flash("Hey, Given emailid is already existed. Try with another.", category="error")
        if len(firstname) < 2:
            flash("Firstname must be 2 charecters", category="error")
        elif len(email) <4:
            flash("Enter Valid Email ID.", category="error")
        elif len(password) < 7:
            flash("Password must be seven charecters", category="error")
        elif password != confirm_password:
            flash("Password doesn't match.", category="error")
        else:
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully!..", category="success")
            # store logged-in details in login_user method. its predefind method from flask
            login_user(user, remember=True)

            # after create user, need to redirect
            return redirect(url_for('views.home'))
    return render_template("signup.html", user = current_user)