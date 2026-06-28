from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.comanda_service import ComandaService
from app.services.mesa_service import MesaService
from app.services.producto_service import ProductoService
from app.services.categoria_producto_service import CategoriaProductoService
from app.services.detalle_comanda_service import DetalleComandaService
from app.utils.decorators import mesero_required

mesero_bp = Blueprint("mesero", __name__)

# ===========================================================================
# DASHBOARD DEL MESERO
# ===========================================================================
@mesero_bp.route("/mesero")
@login_required
@mesero_required
def dashboard():
    """Panel principal del mesero"""
    mesas_disponibles = MesaService.listar_disponibles()
    comandas_activas = ComandaService.listar_abiertas()
    # Filtrar solo las comandas del mesero actual
    mis_comandas = [c for c in comandas_activas if c.id_mesero == current_user.id_usuario]
    
    return render_template(
        "mesero/dashboard.html",
        mesas_disponibles=mesas_disponibles,
        comandas_activas=mis_comandas
    )



# ===========================================================================
# LISTA DE COMANDAS
# ===========================================================================
@mesero_bp.route("/mesero/comandas")
@login_required
@mesero_required
def comandas():
    """Lista de comandas del mesero"""
    comandas = ComandaService.listar_por_mesero(current_user.id_usuario)
    return render_template("mesero/comandas.html", comandas=comandas)

# ===========================================================================
# CREAR NUEVA COMANDA
# ===========================================================================
@mesero_bp.route("/mesero/comanda/nueva", methods=["GET", "POST"])
@login_required
@mesero_required
def nueva_comanda():
    """Crear una nueva comanda"""
    mesas = MesaService.listar_disponibles()
    categorias = CategoriaProductoService.listar_activas()
    productos = ProductoService.listar_activos()
    
    if request.method == "POST":
        id_mesa = request.form.get("id_mesa", type=int)
        notas = request.form.get("notas", "")
        
        # ✅ CORREGIDO: ComandaService.crear() retorna (bool, str)
        exito, mensaje = ComandaService.crear(
            id_mesa=id_mesa,
            id_mesero=current_user.id_usuario,
            notas=notas
        )
        
        flash(mensaje, "success" if exito else "error")
        if exito:
            # ✅ Obtener la última comanda creada por este mesero
            from app.models.comanda import Comanda
            ultima_comanda = Comanda.query.filter_by(
                id_mesero=current_user.id_usuario, 
                estado='abierta'
            ).order_by(Comanda.id_comanda.desc()).first()
            
            if ultima_comanda:
                return redirect(url_for("mesero.ver_comanda", id_comanda=ultima_comanda.id_comanda))
            else:
                return redirect(url_for("mesero.comandas"))
    
    return render_template(
        "mesero/crear_comanda.html",
        mesas=mesas,
        categorias=categorias,
        productos=productos
    )
# ===========================================================================
# VER DETALLE DE COMANDA
# ===========================================================================
@mesero_bp.route("/mesero/comanda/<int:id_comanda>")
@login_required
@mesero_required
def ver_comanda(id_comanda):
    """Ver detalle de una comanda"""
    from app.models.comanda import Comanda
    comanda = Comanda.query.get(id_comanda)
    
    if not comanda:
        flash("Comanda no encontrada.", "error")
        return redirect(url_for("mesero.comandas"))
    
    # Verificar que sea del mesero actual o admin
    if comanda.id_mesero != current_user.id_usuario and current_user.id_rol != 1:
        flash("No tienes permiso para ver esta comanda.", "error")
        return redirect(url_for("mesero.comandas"))
    
    productos = ProductoService.listar_activos()
    categorias = CategoriaProductoService.listar_activas()
    
    return render_template(
        "mesero/ver_comanda.html",
        comanda=comanda,
        productos=productos,
        categorias=categorias
    )

# ===========================================================================
# AGREGAR PRODUCTO A COMANDA
# ===========================================================================
@mesero_bp.route("/mesero/comanda/<int:id_comanda>/agregar", methods=["POST"])
@login_required
@mesero_required
def agregar_producto(id_comanda):
    """Agregar producto a la comanda"""
    id_producto = request.form.get("id_producto", type=int)
    cantidad = request.form.get("cantidad", type=int, default=1)
    notas = request.form.get("notas", "")
    
    exito, mensaje = ComandaService.agregar_producto(
        id_comanda=id_comanda,
        id_producto=id_producto,
        cantidad=cantidad,
        notas=notas
    )
    
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesero.ver_comanda", id_comanda=id_comanda))

# ===========================================================================
# ELIMINAR PRODUCTO DE COMANDA
# ===========================================================================
@mesero_bp.route("/mesero/comanda/<int:id_comanda>/eliminar/<int:id_detalle>")
@login_required
@mesero_required
def eliminar_producto(id_comanda, id_detalle):
    """Eliminar producto de la comanda"""
    exito, mensaje = ComandaService.eliminar_producto(id_detalle)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesero.ver_comanda", id_comanda=id_comanda))

# ===========================================================================
# CERRAR COMANDA
# ===========================================================================
@mesero_bp.route("/mesero/comanda/<int:id_comanda>/cerrar")
@login_required
@mesero_required
def cerrar_comanda(id_comanda):
    """Cerrar una comanda"""
    exito, mensaje = ComandaService.cerrar(id_comanda)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("mesero.comandas"))

# ===========================================================================
# VER MENÚ DE PRODUCTOS
# ===========================================================================
@mesero_bp.route("/mesero/menu")
@login_required
@mesero_required
def menu():
    """Ver menú de productos disponibles"""
    categorias = CategoriaProductoService.listar_activas()
    productos = ProductoService.listar_activos()
    return render_template(
        "mesero/menu.html",
        categorias=categorias,
        productos=productos
    )