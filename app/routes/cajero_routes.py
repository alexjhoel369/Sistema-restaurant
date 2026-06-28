from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import cajero_required
from app.services.caja_sesion_service import CajaSesionService
from app.services.factura_service import FacturaService
from app.services.comanda_service import ComandaService
from app.services.cliente_service import ClienteService
from app.services.metodo_pago_service import MetodoPagoService
from app.models.caja_sesion import CajaSesion

cajero_bp = Blueprint("cajero", __name__)

# ===========================================================================
# DASHBOARD DEL CAJERO
# ===========================================================================
@cajero_bp.route("/cajero")
@login_required
@cajero_required
def dashboard():
    """Panel principal del cajero"""
    from app.models.comanda import Comanda
    from app.models.factura import Factura
    
    sesion_activa = CajaSesionService.obtener_sesion_activa()
    
    # ✅ Comandas cerradas que NO tienen factura asociada
    comandas_cerradas = Comanda.query.filter_by(estado='cerrada').order_by(
        Comanda.fecha_cierre.desc()
    ).all()
    
    # Filtrar las que ya fueron facturadas
    comandas_sin_facturar = []
    for comanda in comandas_cerradas:
        factura_existente = Factura.query.filter_by(id_comanda=comanda.id_comanda).first()
        if not factura_existente:
            comandas_sin_facturar.append(comanda)
    
    return render_template(
        "cajero/dashboard.html",
        sesion_activa=sesion_activa,
        comandas_cerradas=comandas_sin_facturar  # Solo las no facturadas
    )

# ===========================================================================
# ABRIR CAJA
# ===========================================================================
@cajero_bp.route("/cajero/abrir-caja", methods=["POST"])
@login_required
@cajero_required
def abrir_caja():
    """Abre una nueva sesión de caja"""
    monto_apertura = request.form.get("monto_apertura", type=float, default=0)
    
    exito, mensaje = CajaSesionService.abrir_sesion(
        id_cajero=current_user.id_usuario,
        monto_apertura=monto_apertura
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cajero.dashboard"))

# ===========================================================================
# CERRAR CAJA
# ===========================================================================
@cajero_bp.route("/cajero/cerrar-caja", methods=["POST"])
@login_required
@cajero_required
def cerrar_caja():
    """Cierra la sesión de caja activa"""
    monto_cierre = request.form.get("monto_cierre", type=float, default=0)
    observaciones = request.form.get("observaciones", "")
    
    sesion = CajaSesionService.obtener_sesion_activa()
    if sesion:
        exito, mensaje = CajaSesionService.cerrar_sesion(
            id_sesion=sesion.id_sesion,
            monto_cierre=monto_cierre,
            observaciones=observaciones
        )
    else:
        exito, mensaje = False, "No hay sesión de caja activa."
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cajero.dashboard"))

# ===========================================================================
# FACTURAR COMANDA
# ===========================================================================
@cajero_bp.route("/cajero/facturar/<int:id_comanda>", methods=["GET", "POST"])
@login_required
@cajero_required
def facturar(id_comanda):
    """Factura una comanda cerrada"""
    from app.models.comanda import Comanda
    comanda = Comanda.query.get(id_comanda)
    
    if not comanda:
        flash("Comanda no encontrada.", "error")
        return redirect(url_for("cajero.dashboard"))
    
    if comanda.estado != 'cerrada':
        flash("Solo se pueden facturar comandas cerradas.", "error")
        return redirect(url_for("cajero.dashboard"))
    
    clientes = ClienteService.listar_activos()
    metodos_pago = MetodoPagoService.listar_activos()
    
    if request.method == "POST":
        nit_ci = request.form.get("nit_ci", "0")
        razon_social = request.form.get("razon_social", "SIN NOMBRE")
        id_metodo_pago = request.form.get("id_metodo_pago", type=int)
        monto_pago = request.form.get("monto_pago", type=float, default=float(comanda.total))
        referencia = request.form.get("referencia", "")
        
        # Obtener sesión activa
        sesion = CajaSesionService.obtener_sesion_activa()
        if not sesion:
            flash("Debe abrir una sesión de caja antes de facturar.", "error")
            return redirect(url_for("cajero.dashboard"))
        
        exito, mensaje, factura = FacturaService.crear_desde_comanda(
            id_comanda=id_comanda,
            id_sesion=sesion.id_sesion,
            nit_ci_cliente=nit_ci,
            razon_social_cliente=razon_social,
            id_metodo_pago=id_metodo_pago,
            monto_pago=monto_pago,
            referencia=referencia
        )
        
        flash(mensaje, "success" if exito else "error")
        if exito:
            return redirect(url_for("cajero.dashboard"))
    
    return render_template(
        "cajero/facturar.html",
        comanda=comanda,
        clientes=clientes,
        metodos_pago=metodos_pago
    )

# ===========================================================================
# VER CLIENTES (SOLO LECTURA)
# ===========================================================================
@cajero_bp.route("/cajero/clientes")
@login_required
@cajero_required
def clientes():
    """Ver lista de clientes (solo lectura)"""
    clientes = ClienteService.listar_activos()
    return render_template("cajero/clientes.html", clientes=clientes)

# ===========================================================================
# HISTORIAL DE FACTURAS
# ===========================================================================
@cajero_bp.route("/cajero/facturas")
@login_required
@cajero_required
def facturas():
    """Ver historial de facturas"""
    from app.models.factura import Factura
    facturas_list = Factura.query.order_by(Factura.fecha_emision.desc()).limit(100).all()
    return render_template("cajero/facturas.html", facturas=facturas_list)