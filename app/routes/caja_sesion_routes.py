from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.models.factura import Factura
from app.models.caja_sesion import CajaSesion
from app.services.caja_sesion_service import CajaSesionService
from decimal import Decimal
from app.utils.decorators import admin_required, cajero_required

caja_bp = Blueprint("caja", __name__)

@caja_bp.route("/caja")
@login_required
@admin_required
def caja():
    sesiones = CajaSesionService.listar()
    return render_template("admin/caja.html", sesiones=sesiones)

@caja_bp.route("/caja/abrir", methods=["POST"])
@login_required
@admin_required
def abrir():
    monto_apertura = request.form.get("monto_apertura")
    
    try:
        monto = float(monto_apertura)
    except (ValueError, TypeError):
        flash("Monto de apertura inválido.", "error")
        return redirect(url_for("caja.caja"))
    
    exito, mensaje = CajaSesionService.abrir_sesion(current_user.id_usuario, monto)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("caja.caja"))

@caja_bp.route("/caja/cerrar/<int:id_sesion>", methods=["POST"])
@login_required
@admin_required
def cerrar(id_sesion):
    monto_cierre = request.form.get("monto_cierre")
    
    try:
        monto = float(monto_cierre)
    except (ValueError, TypeError):
        flash("Monto de cierre inválido.", "error")
        return redirect(url_for("caja.caja"))
        
    exito, mensaje = CajaSesionService.cerrar_sesion(id_sesion, monto)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("caja.caja"))

@caja_bp.route("/cajero/dashboard")
@login_required
@cajero_required
def cajero_dashboard():
    sesion_activa = CajaSesion.query.filter_by(
        id_cajero=current_user.id_usuario,
        estado='abierta'
    ).order_by(CajaSesion.fecha_apertura.desc()).first()
    
    facturas_sesion = []
    total_acumulado = Decimal('0.00')
    
    if sesion_activa:
        facturas_sesion = Factura.query.filter_by(
            id_sesion=sesion_activa.id_sesion,
            estado='valida'
        ).order_by(Factura.fecha.desc()).all()
        
        total_acumulado = sum(f.total for f in facturas_sesion)
    
    return render_template("cajero/dashboard.html", 
                           sesion_activa=sesion_activa,
                           facturas_sesion=facturas_sesion,
                           total_acumulado=total_acumulado)