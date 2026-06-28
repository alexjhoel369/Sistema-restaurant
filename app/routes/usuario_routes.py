from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.usuario_service import UsuarioService
from app.services.rol_service import RolService
from app.utils.decorators import admin_required

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuarios")
@login_required
@admin_required
def usuarios():
    usuarios = UsuarioService.listar()
    roles = RolService.listar()
    return render_template("admin/usuarios.html", usuarios=usuarios, roles=roles, editar=None)

@usuario_bp.route("/usuarios/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    email = request.form.get("email")
    password = request.form.get("password")
    id_rol = request.form.get("id_rol")
    telefono = request.form.get("telefono")
    
    exito, mensaje = UsuarioService.crear(nombre, apellido, email, password, id_rol, telefono)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("usuario.usuarios"))

@usuario_bp.route("/usuarios/editar/<int:id_usuario>")
@login_required
@admin_required
def editar(id_usuario):
    editar = UsuarioService.obtener(id_usuario)
    if not editar:
        flash("El usuario solicitado no existe.", "error")
        return redirect(url_for("usuario.usuarios"))
    usuarios = UsuarioService.listar()
    roles = RolService.listar()
    return render_template("admin/usuarios.html", usuarios=usuarios, roles=roles, editar=editar)

@usuario_bp.route("/usuarios/actualizar/<int:id_usuario>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_usuario):
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    email = request.form.get("email")
    id_rol = request.form.get("id_rol")
    activo = request.form.get("activo") == 'on'
    telefono = request.form.get("telefono")
    password = request.form.get("password")
    
    exito, mensaje = UsuarioService.actualizar(id_usuario, nombre, apellido, email, id_rol, activo, telefono, password)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("usuario.usuarios"))

@usuario_bp.route("/usuarios/eliminar/<int:id_usuario>")
@login_required
@admin_required
def eliminar(id_usuario):
    exito, mensaje = UsuarioService.eliminar(id_usuario)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("usuario.usuarios"))