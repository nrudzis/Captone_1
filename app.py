"""Stocks application."""

from flask import Flask, redirect, render_template, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stocks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_home():
    """Redirect to /home."""
    return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def show_home():
    """Show home page."""

    if 'username' not in session:
        login_form = LoginForm()
        register_form = RegisterForm()
        if login_form.validate_on_submit() and login_form.login_submit.data:
            username = login_form.username.data
            password = login_form.password.data
            user = User.authenticate(username, password)
            if user:
                session['username'] = user.username
                return redirect('/home')
            else:
                login_form.username.errors = ['Username or password is invalid.']
        elif register_form.validate_on_submit() and register_form.register_submit.data:
            email = register_form.email.data
            username = register_form.username.data
            password = register_form.password.data
            new_user = User.register(email, username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect('/home')
        else:
            return render_template('logged-out-home.html', login_form=login_form, register_form=register_form)
    else:
        return render_template('logged-in-home.html')