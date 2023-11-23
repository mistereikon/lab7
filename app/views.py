from flask import render_template, redirect, url_for, flash
from app import db
from app.forms import RegistrationForm
from app.models import User
from flask_login import login_user, logout_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from app.forms import LoginForm

from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    users = User.get_all_users()
    total_users = len(users)
    return render_template('index.html', users=users, total_users=total_users)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Ви вже увійшли в обліковий запис!', 'info')
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш обліковий запис створено! Тепер ви можете увійти.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title='Реєстрація', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False) 
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Не вдалося увійти. Перевірте логін та пароль.', 'danger')
    return render_template('login.html', title='Вхід', form=form)

@bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Ви вийшли з облікового запису', 'info')
    return redirect(url_for('main.index'))

@bp.route('/account')
@login_required
def account():
    return render_template('account.html', title='Аккаунт')


