from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.forms import LoginForm
from app.models import User
from app import db
from datetime import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion admin"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Ce compte est désactivé.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('admin.dashboard')
        
        flash(f'Bienvenue, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))
