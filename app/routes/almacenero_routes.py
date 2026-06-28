from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import almacenero_required
from app.services.insumo_service import InsumoService
from app.services.inventario_movimiento_service import InventarioMovimientoService
from app.services.proveedor_service import ProveedorService

almacenero_bp = Blueprint("almacenero", __name__)

# ===========================================================================
# DASHBOARD DEL ALMACENERO
# ===========================================================================
@almacenero_bp.route("/almacenero")
@login_required
@almacenero_required
def dashboard():
    """Panel principal del almacenero"""
    # ✅ Pasar TODOS los insumos para los formularios
    todos_insumos = InsumoService.listar_activos()
    insumos_bajos = InsumoService.listar_stock_bajo()
    movimientos_recientes = InventarioMovimientoService.listar()[:50]
    proveedores = ProveedorService.listar_activos()
    
    return render_template(
        "almacenero/dashboard.html",
        insumos_bajos=insumos_bajos,
        todos_insumos=todos_insumos,  # ✅ Nueva variable
        movimientos_recientes=movimientos_recientes,
        proveedores=proveedores
    )

# ===========================================================================
# REGISTRAR ENTRADA DE INVENTARIO
# ===========================================================================
@almacenero_bp.route("/almacenero/entrada", methods=["POST"])
@login_required
@almacenero_required
def registrar_entrada():
    """Registra una entrada de compra"""
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    costo_unitario = request.form.get("costo_unitario", type=float, default=0)
    id_proveedor = request.form.get("id_proveedor", type=int)
    numero_factura = request.form.get("numero_factura", "")
    motivo = request.form.get("motivo", "")
    
    exito, mensaje = InventarioMovimientoService.crear_entrada_compra(
        id_insumo=id_insumo,
        cantidad=cantidad,
        costo_unitario=costo_unitario,
        id_proveedor=id_proveedor,
        id_usuario=current_user.id_usuario,
        numero_factura=numero_factura,
        motivo=motivo
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("almacenero.dashboard"))

# ===========================================================================
# REGISTRAR SALIDA DE INVENTARIO
# ===========================================================================
@almacenero_bp.route("/almacenero/salida", methods=["POST"])
@login_required
@almacenero_required
def registrar_salida():
    """Registra una salida por merma"""
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    motivo = request.form.get("motivo", "")
    
    exito, mensaje = InventarioMovimientoService.crear_salida_merma(
        id_insumo=id_insumo,
        cantidad=cantidad,
        id_usuario=current_user.id_usuario,
        motivo=motivo
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("almacenero.dashboard"))

# ===========================================================================
# REGISTRAR AJUSTE DE INVENTARIO
# ===========================================================================
@almacenero_bp.route("/almacenero/ajuste", methods=["POST"])
@login_required
@almacenero_required
def registrar_ajuste():
    """Registra un ajuste de inventario"""
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    motivo = request.form.get("motivo", "")
    
    exito, mensaje = InventarioMovimientoService.crear_ajuste(
        id_insumo=id_insumo,
        cantidad=cantidad,
        id_usuario=current_user.id_usuario,
        motivo=motivo
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("almacenero.dashboard"))

# ===========================================================================
# VER KARDEX DE INSUMO
# ===========================================================================
@almacenero_bp.route("/almacenero/kardex/<int:id_insumo>")
@login_required
@almacenero_required
def kardex(id_insumo):
    """Ver historial de movimientos de un insumo"""
    insumo = InsumoService.obtener(id_insumo)
    if not insumo:
        flash("Insumo no encontrado.", "error")
        return redirect(url_for("almacenero.dashboard"))
    
    movimientos = InventarioMovimientoService.obtener_kardex(id_insumo)
    return render_template(
        "almacenero/kardex.html",
        insumo=insumo,
        movimientos=movimientos
    )