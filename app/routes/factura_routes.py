from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.factura_service import FacturaService
from app.services.comanda_service import ComandaService
from app.services.caja_sesion_service import CajaSesionService
from app.utils.decorators import cajero_required, admin_required

factura_bp = Blueprint("factura", __name__)

@factura_bp.route("/facturas")
@login_required
@admin_required
def facturas():
    facturas = FacturaService.listar()
    return render_template("admin/facturas.html", facturas=facturas)

@factura_bp.route("/facturas/generar/<int:id_comanda>")
@login_required
@cajero_required
def generar_form(id_comanda):
    comanda = ComandaService.obtener(id_comanda)
    if not comanda:
        flash("Comanda no encontrada.", "error")
        return redirect(url_for("comanda.comandas"))
    
    sesiones = CajaSesionService.listar()
    sesion_activa = next((s for s in sesiones if s.estado == 'abierta'), None)
    
    if not sesion_activa:
        flash("No hay una sesión de caja abierta.", "error")
        return redirect(url_for("caja.caja"))

    return render_template("admin/generar_factura.html", comanda=comanda, sesion=sesion_activa)

@factura_bp.route("/facturas/guardar", methods=["POST"])
@login_required
@cajero_required
def guardar():
    id_comanda = request.form.get("id_comanda")
    id_sesion = request.form.get("id_sesion")
    nit_ci = request.form.get("nit_ci")
    razon_social = request.form.get("razon_social")
    
    pagos = [{
        "metodo_pago": request.form.get("metodo_pago"), 
        "monto": request.form.get("total")
    }]

    exito, mensaje = FacturaService.generar_factura(
        int(id_comanda), 
        int(id_sesion), 
        nit_ci, 
        razon_social, 
        pagos,
        id_usuario=current_user.id_usuario
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("factura.facturas"))

@factura_bp.route("/facturas/anular/<int:id_factura>")
@login_required
@admin_required
def anular(id_factura):
    exito, mensaje = FacturaService.anular(id_factura)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("factura.facturas"))