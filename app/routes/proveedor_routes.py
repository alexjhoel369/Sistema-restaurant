from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.proveedor_service import ProveedorService
from app.utils.decorators import admin_required

proveedor_bp = Blueprint("proveedor", __name__)

@proveedor_bp.route("/proveedores")
@login_required
@admin_required
def proveedores():
    proveedores = ProveedorService.listar()
    return render_template("admin/proveedores.html", proveedores=proveedores, editar=None)

@proveedor_bp.route("/proveedores/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    nombre = request.form.get("nombre")
    nit_ci = request.form.get("nit_ci")
    telefono = request.form.get("telefono")
    email = request.form.get("email")
    direccion = request.form.get("direccion")
    contacto_nombre = request.form.get("contacto_nombre")
    
    exito, mensaje = ProveedorService.crear(nombre, nit_ci, telefono, email, direccion, contacto_nombre)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("proveedor.proveedores"))

@proveedor_bp.route("/proveedores/editar/<int:id_proveedor>")
@login_required
@admin_required
def editar(id_proveedor):
    editar = ProveedorService.obtener(id_proveedor)
    if not editar:
        flash("El proveedor solicitado no existe.", "error")
        return redirect(url_for("proveedor.proveedores"))
    proveedores = ProveedorService.listar()
    return render_template("admin/proveedores.html", proveedores=proveedores, editar=editar)

@proveedor_bp.route("/proveedores/actualizar/<int:id_proveedor>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_proveedor):
    nombre = request.form.get("nombre")
    nit_ci = request.form.get("nit_ci")
    telefono = request.form.get("telefono")
    email = request.form.get("email")
    direccion = request.form.get("direccion")
    contacto_nombre = request.form.get("contacto_nombre")
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = ProveedorService.actualizar(id_proveedor, nombre, nit_ci, telefono, email, direccion, contacto_nombre, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("proveedor.proveedores"))

@proveedor_bp.route("/proveedores/eliminar/<int:id_proveedor>")
@login_required
@admin_required
def eliminar(id_proveedor):
    exito, mensaje = ProveedorService.eliminar(id_proveedor)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("proveedor.proveedores"))