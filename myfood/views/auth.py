from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from ..models import User, Role, Permission
from ..forms import LoginForm, RegistrationForm
from .. import db

mod = Blueprint('auth', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('auth/login.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, nickname = form.nickname.data, password = form.password.data)
        db.session.add(user)
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@mod.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
