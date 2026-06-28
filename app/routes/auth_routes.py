from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.services.usuario_service import UsuarioService

auth_bp = Blueprint("auth", __name__)

# ===========================================================================
# RUTA PRINCIPAL - PÁGINA DE INICIO
# ===========================================================================
@auth_bp.route("/")
def index():
    """Página principal - Redirige según autenticación"""
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("auth.login"))

# ===========================================================================
# INICIO DE SESIÓN
# ===========================================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya está autenticado, redirigir al dashboard
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == 'on'
        
        # Validar campos
        if not email or not password:
            flash("Por favor complete todos los campos.", "error")
            return render_template("auth/login.html")
        
        # Buscar usuario
        usuario = UsuarioService.obtener_por_email(email)
        
        if not usuario:
            flash("Email o contraseña incorrectos.", "error")
            return render_template("auth/login.html")
        
        # Verificar si el usuario está activo
        if not usuario.activo:
            flash("Tu cuenta está desactivada. Contacta al administrador.", "error")
            return render_template("auth/login.html")
        
        # Verificar contraseña
        if check_password_hash(usuario.contraseña_hash, password):
            login_user(usuario, remember=remember)
            flash(f"¡Bienvenido {usuario.nombre}!", "success")
            
            # ✅ REDIRIGIR SEGÚN ROL (CORREGIDO)
            rol_id = usuario.id_rol
            
            if rol_id == 1:  # Administrador
                return redirect(url_for("admin.dashboard"))
            elif rol_id == 2:  # Gerente
                return redirect(url_for("admin.dashboard"))
            elif rol_id == 3:  # Cajero
                return redirect(url_for("cajero.dashboard"))  
            elif rol_id == 4:  # Mesero
                return redirect(url_for("mesero.dashboard"))
            elif rol_id == 5:  # Cocinero
                return redirect(url_for("cocinero.dashboard"))  
            elif rol_id == 6:  # Almacenero
                return redirect(url_for("almacenero.dashboard"))
            else:
                return redirect(url_for("admin.dashboard"))
        else:
            flash("Email o contraseña incorrectos.", "error")
    
    return render_template("auth/login.html")

# ===========================================================================
# CERRAR SESIÓN
# ===========================================================================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for("auth.login"))

# ===========================================================================
# MANEJADORES DE ERRORES
# ===========================================================================
@auth_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@auth_bp.app_errorhandler(500)
def internal_server_error(e):
    from app import db
    db.session.rollback()
    return render_template("errors/500.html"), 500