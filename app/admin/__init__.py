from flask import Blueprint
from flask_login import login_required, current_user

bp = Blueprint('admin', __name__)

@bp.before_request
@login_required
def before_request():
    """Vérifier que l'utilisateur est admin"""
    if not current_user.is_authenticated or not current_user.is_admin:
        from flask import flash, redirect, url_for
        flash('Accès réservé aux administrateurs.', 'error')
        return redirect(url_for('auth.login'))

from app.admin import routes
