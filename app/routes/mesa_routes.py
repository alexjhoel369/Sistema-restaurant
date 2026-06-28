from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.mesa_service import MesaService
from app.utils.decorators import admin_required

mesa_bp = Blueprint("mesa", __name__)

@mesa_bp.route("/mesas")
@login_required
@admin_required
def mesas():
    mesas = MesaService.listar()
    return render_template("admin/mesas.html", mesas=mesas, editar=None)

@mesa_bp.route("/mesas/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    numero = request.form.get("numero")
    capacidad = request.form.get("capacidad", type=int)
    ubicacion = request.form.get("ubicacion")
    
    exito, mensaje = MesaService.crear(numero, capacidad, ubicacion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesa.mesas"))

@mesa_bp.route("/mesas/editar/<int:id_mesa>")
@login_required
@admin_required
def editar(id_mesa):
    editar = MesaService.obtener(id_mesa)
    if not editar:
        flash("La mesa solicitada no existe.", "error")
        return redirect(url_for("mesa.mesas"))
    mesas = MesaService.listar()
    return render_template("admin/mesas.html", mesas=mesas, editar=editar)

@mesa_bp.route("/mesas/actualizar/<int:id_mesa>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_mesa):
    numero = request.form.get("numero")
    capacidad = request.form.get("capacidad", type=int)
    ubicacion = request.form.get("ubicacion")
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = MesaService.actualizar(id_mesa, numero, capacidad, ubicacion, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesa.mesas"))

@mesa_bp.route("/mesas/eliminar/<int:id_mesa>")
@login_required
@admin_required
def eliminar(id_mesa):
    exito, mensaje = MesaService.eliminar(id_mesa)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesa.mesas"))