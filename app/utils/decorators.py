from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Decorador para rutas que requieren rol de Administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id_rol != 1:
            flash("Acceso denegado. Se requiere rol de Administrador.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def mesero_required(f):
    """Decorador para rutas que requieren rol de Mesero"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id_rol not in [1, 4]:
            flash("Acceso denegado. Se requiere rol de Mesero.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def cajero_required(f):
    """Decorador para rutas que requieren rol de Cajero"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id_rol not in [1, 3]:
            flash("Acceso denegado. Se requiere rol de Cajero.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def cocinero_required(f):
    """Decorador para rutas que requieren rol de Cocinero"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id_rol not in [1, 5]:
            flash("Acceso denegado. Se requiere rol de Cocinero.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def almacenero_required(f):
    """Decorador para rutas que requieren rol de Almacenero"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id_rol not in [1, 6]:
            flash("Acceso denegado. Se requiere rol de Almacenero.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function