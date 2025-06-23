from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logueado') or session.get('id_rol') != 1:
            flash('No tienes permisos para acceder a esta página.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def usuario_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logueado') or session.get('id_rol') != 2:
            flash('No tienes permisos para acceder a esta página.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated
