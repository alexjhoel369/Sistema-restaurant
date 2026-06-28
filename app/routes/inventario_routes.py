from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.inventario_movimiento_service import InventarioMovimientoService
from app.services.insumo_service import InsumoService
from app.services.proveedor_service import ProveedorService
from app.utils.decorators import admin_required

inventario_bp = Blueprint("inventario", __name__)

@inventario_bp.route("/inventario")
@login_required
@admin_required
def inventario():
    """Vista principal de inventario"""
    insumos = InsumoService.listar_activos()
    movimientos = InventarioMovimientoService.listar()[:100]  # Últimos 100 movimientos
    return render_template("admin/inventario.html", insumos=insumos, movimientos=movimientos)

@inventario_bp.route("/inventario/movimientos")
@login_required
@admin_required
def movimientos():
    movimientos = InventarioMovimientoService.listar()
    return render_template("admin/inventario_movimientos.html", movimientos=movimientos)

@inventario_bp.route("/inventario/entrada", methods=["POST"])
@login_required
@admin_required
def registrar_entrada():
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    costo_unitario = request.form.get("costo_unitario", type=float)
    id_proveedor = request.form.get("id_proveedor", type=int)
    numero_factura = request.form.get("numero_factura")
    motivo = request.form.get("motivo")
    
    exito, mensaje = InventarioMovimientoService.crear_entrada_compra(
        id_insumo, cantidad, costo_unitario, id_proveedor, current_user.id_usuario, numero_factura, motivo
    )
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("inventario.inventario"))

@inventario_bp.route("/inventario/salida", methods=["POST"])
@login_required
@admin_required
def registrar_salida():
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    motivo = request.form.get("motivo")
    
    exito, mensaje = InventarioMovimientoService.crear_salida_merma(
        id_insumo, cantidad, current_user.id_usuario, motivo
    )
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("inventario.inventario"))

@inventario_bp.route("/inventario/ajuste", methods=["POST"])
@login_required
@admin_required
def registrar_ajuste():
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad = request.form.get("cantidad", type=float)
    motivo = request.form.get("motivo")
    
    exito, mensaje = InventarioMovimientoService.crear_ajuste(
        id_insumo, cantidad, current_user.id_usuario, motivo
    )
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("inventario.inventario"))

@inventario_bp.route("/inventario/kardex/<int:id_insumo>")
@login_required
@admin_required
def kardex(id_insumo):
    insumo = InsumoService.obtener(id_insumo)
    if not insumo:
        flash("El insumo no existe.", "error")
        return redirect(url_for("inventario.inventario"))
    
    movimientos = InventarioMovimientoService.obtener_kardex(id_insumo)
    return render_template("admin/inventario_kardex.html", insumo=insumo, movimientos=movimientos)