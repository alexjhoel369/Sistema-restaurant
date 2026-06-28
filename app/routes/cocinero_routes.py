from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import cocinero_required
from app.services.detalle_comanda_service import DetalleComandaService
from app.services.receta_service import RecetaService
from app.services.producto_service import ProductoService

cocinero_bp = Blueprint("cocinero", __name__)

# ===========================================================================
# DASHBOARD DEL COCINERO
# ===========================================================================
@cocinero_bp.route("/cocinero")
@login_required
@cocinero_required
def dashboard():
    """Panel principal del cocinero - Muestra productos pendientes"""
    from app.models.detalle_comanda import DetalleComanda
    from app.models.comanda import Comanda
    
    # Obtener todos los detalles pendientes y en preparación
    pendientes = DetalleComanda.query.filter(
        DetalleComanda.estado_preparacion.in_(['pendiente', 'en_preparacion'])
    ).join(Comanda).filter(
        Comanda.estado == 'abierta'
    ).order_by(DetalleComanda.id_detalle).all()
    
    return render_template("cocinero/dashboard.html", pendientes=pendientes)

# ===========================================================================
# CAMBIAR ESTADO DE PREPARACIÓN
# ===========================================================================
@cocinero_bp.route("/cocinero/cambiar-estado/<int:id_detalle>/<string:nuevo_estado>")
@login_required
@cocinero_required
def cambiar_estado(id_detalle, nuevo_estado):
    """Cambia el estado de preparación de un producto"""
    exito, mensaje = DetalleComandaService.cambiar_estado(id_detalle, nuevo_estado)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("cocinero.dashboard"))

# ===========================================================================
# VER RECETA DE UN PRODUCTO
# ===========================================================================
@cocinero_bp.route("/cocinero/receta/<int:id_producto>")
@login_required
@cocinero_required
def ver_receta(id_producto):
    """Muestra la receta de un producto específico"""
    producto = ProductoService.obtener(id_producto)
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("cocinero.dashboard"))
    
    recetas = RecetaService.listar_por_producto(id_producto)
    return render_template("cocinero/ver_receta.html", producto=producto, recetas=recetas)