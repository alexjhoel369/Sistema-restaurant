from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.cliente_service import ClienteService
from app.utils.decorators import admin_required

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes")
@login_required
@admin_required
def clientes():
    clientes = ClienteService.listar()
    return render_template("admin/clientes.html", clientes=clientes, editar=None)

@cliente_bp.route("/clientes/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    tipo_documento = request.form.get("tipo_documento", "CI")
    nit_ci = request.form.get("nit_ci")
    razon_social = request.form.get("razon_social")
    complemento = request.form.get("complemento")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    direccion = request.form.get("direccion")
    
    exito, mensaje = ClienteService.crear(tipo_documento, nit_ci, razon_social, complemento, email, telefono, direccion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cliente.clientes"))

@cliente_bp.route("/clientes/editar/<int:id_cliente>")
@login_required
@admin_required
def editar(id_cliente):
    editar = ClienteService.obtener(id_cliente)
    if not editar:
        flash("El cliente solicitado no existe.", "error")
        return redirect(url_for("cliente.clientes"))
    clientes = ClienteService.listar()
    return render_template("admin/clientes.html", clientes=clientes, editar=editar)

@cliente_bp.route("/clientes/actualizar/<int:id_cliente>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_cliente):
    tipo_documento = request.form.get("tipo_documento", "CI")
    nit_ci = request.form.get("nit_ci")
    razon_social = request.form.get("razon_social")
    complemento = request.form.get("complemento")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    direccion = request.form.get("direccion")
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = ClienteService.actualizar(id_cliente, tipo_documento, nit_ci, razon_social, complemento, email, telefono, direccion, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cliente.clientes"))

@cliente_bp.route("/clientes/eliminar/<int:id_cliente>")
@login_required
@admin_required
def eliminar(id_cliente):
    exito, mensaje = ClienteService.eliminar(id_cliente)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cliente.clientes"))