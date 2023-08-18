from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('The email is already associated with us. Kindly sign-up with different email or sign-in to continue', category='error')
        elif len(email) < 4:
            flash('The provided email address is invalid. Please provide a legitimate email address', category='error')
        elif len(password1) < 7 and len(password2) < 7:
            flash('Password should be greater than(or equals to) 7 characters.', category='error')
        elif password1 != password2:
            flash('Password provided by you didn\'t matched. Either one of the password is incorrect.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastName=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Congrats! You\'re Signed up successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)

@auth.route("/sign-in", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are signed-in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Credentials. Kindly try again!', category='error')
        else:
            flash('The email seems to be new to me. Kindly associate the email with the system!', category='error')

    return render_template('sign-in.html', user=current_user)

@auth.route("/log-out")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))
