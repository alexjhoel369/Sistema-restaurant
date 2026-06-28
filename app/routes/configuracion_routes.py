from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.configuracion_service import ConfiguracionService
from app.utils.decorators import admin_required

configuracion_bp = Blueprint("configuracion", __name__)

@configuracion_bp.route("/configuracion")
@login_required
@admin_required
def configuracion():
    configuraciones = ConfiguracionService.listar()
    return render_template("admin/configuracion.html", configuraciones=configuraciones, editar=None)

@configuracion_bp.route("/configuracion/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    clave = request.form.get("clave")
    valor = request.form.get("valor")
    descripcion = request.form.get("descripcion")
    tipo = request.form.get("tipo", "texto")
    editable = request.form.get("editable") == 'on'
    
    exito, mensaje = ConfiguracionService.crear(clave, valor, descripcion, tipo, editable)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("configuracion.configuracion"))

@configuracion_bp.route("/configuracion/editar/<int:id_config>")
@login_required
@admin_required
def editar(id_config):
    editar = ConfiguracionService.obtener(id_config)
    if not editar:
        flash("La configuración no existe.", "error")
        return redirect(url_for("configuracion.configuracion"))
    configuraciones = ConfiguracionService.listar()
    return render_template("admin/configuracion.html", configuraciones=configuraciones, editar=editar)

@configuracion_bp.route("/configuracion/actualizar/<int:id_config>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_config):
    valor = request.form.get("valor")
    descripcion = request.form.get("descripcion")
    
    exito, mensaje = ConfiguracionService.actualizar(id_config, valor, descripcion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("configuracion.configuracion"))

@configuracion_bp.route("/configuracion/eliminar/<int:id_config>")
@login_required
@admin_required
def eliminar(id_config):
    exito, mensaje = ConfiguracionService.eliminar(id_config)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("configuracion.configuracion"))