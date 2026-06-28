from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.inventario_movimiento_service import InventarioMovimientoService
from app.services.insumo_service import InsumoService
from app.services.proveedor_service import ProveedorService
from app.models.inventario_movimiento import InventarioMovimiento
from sqlalchemy.orm import joinedload
from app.utils.decorators import admin_required

inventario_bp = Blueprint("inventario", __name__)

@inventario_bp.route("/inventario/movimientos")
@login_required
@admin_required
def movimientos():
    todos_movimientos = InventarioMovimiento.query.options(
        joinedload(InventarioMovimiento.insumo),
        joinedload(InventarioMovimiento.proveedor),
        joinedload(InventarioMovimiento.usuario)
    ).order_by(InventarioMovimiento.fecha.desc()).all()

    insumos = InsumoService.listar()
    proveedores = ProveedorService.listar()

    return render_template("admin/movimientos_inventario.html", 
                           movimientos=todos_movimientos, 
                           insumos=insumos, 
                           proveedores=proveedores)

@inventario_bp.route("/inventario/registrar", methods=["POST"])
@login_required
@admin_required
def registrar():
    id_insumo = request.form.get("id_insumo")
    tipo = request.form.get("tipo")
    cantidad = request.form.get("cantidad")
    id_proveedor = request.form.get("id_proveedor")
    
    prov_id = int(id_proveedor) if id_proveedor and id_proveedor.strip() != "" else None
    
    try:
        exito, mensaje = InventarioMovimientoService.registrar_movimiento(
            int(id_insumo), 
            tipo, 
            float(cantidad), 
            current_user.id_usuario,  # CORRECCIÓN: Usar current_user
            prov_id
        )
    except (ValueError, TypeError):
        flash("Datos de movimiento inválidos.", "error")
        return redirect(url_for("inventario.movimientos"))
        
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("inventario.movimientos"))