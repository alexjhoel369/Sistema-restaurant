from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.rol_service import RolService
from app.utils.decorators import admin_required

rol_bp = Blueprint("rol", __name__)

@rol_bp.route("/roles")
@login_required
@admin_required
def roles():
    roles = RolService.listar()
    return render_template("admin/roles.html", roles=roles, editar=None)

@rol_bp.route("/roles/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    exito, mensaje = RolService.crear(nombre, descripcion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("rol.roles"))

@rol_bp.route("/roles/editar/<int:id_rol>")
@login_required
@admin_required
def editar(id_rol):
    editar = RolService.obtener(id_rol)
    if not editar:
        flash("El rol que intentas editar no existe.", "error")
        return redirect(url_for("rol.roles"))
    roles = RolService.listar()
    return render_template("admin/roles.html", roles=roles, editar=editar)

@rol_bp.route("/roles/actualizar/<int:id_rol>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_rol):
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    exito, mensaje = RolService.actualizar(id_rol, nombre, descripcion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("rol.roles"))

@rol_bp.route("/roles/eliminar/<int:id_rol>")
@login_required
@admin_required
def eliminar(id_rol):
    exito, mensaje = RolService.eliminar(id_rol)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("rol.roles"))