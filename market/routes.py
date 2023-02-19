from market import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from market import db
from .models import Item, User
from .forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register',  methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form.get("username")  # or form.username.data
        email_address = request.form.get("email_address")
        password1 = request.form.get("password1")

        check_email = User.query.filter_by(email_address=email_address).first()
        check_username = User.query.filter_by(username=username).first()

        if check_username:
            flash("Username already exists! Please try a different username", category="danger")
            return redirect(url_for("register_page"))
        elif check_email:
            flash("Email already exists! Please try a different email", category="danger")
            return redirect(url_for("register_page"))
        else:
            user = User(username, email_address, password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login_page"))

    else:
        for err in form.errors.values():
            flash(err[0], category="danger")

    return render_template('register.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if attempted_user and check_password_hash(attempted_user.password, form.password.data):
            login_user(attempted_user)
            flash(f"Success! Welcome {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash('Username and password are not match! Please try again', category="danger")
            return redirect(url_for("login_page"))
    return render_template("login.html", form=form)

########################
# WITHOUT login_user but login_user has advantage us to control on our user authentication
########################

# @app.route('/login', methods=["GET", "POST"])
# def login_page():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = request.form.get("username")
#         password = request.form.get("password")
#         user = User.query.filter_by(username=username).first()
#         # check if the user actually exists
#         # take the user-supplied password, hash it, and compare it to the hashed password in the database
#         if not user or not check_password_hash(user.password, password):
#             flash('Username and password are not match! Please try again', category="danger")
#             return redirect(url_for("login_page"))
#         else:
#             flash(f"Success! Welcome {username}", category="success")
#             return redirect(url_for("market_page"))
#
#     return render_template("login.html", form=form)