from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.comanda_service import ComandaService
from app.services.mesa_service import MesaService
from app.services.usuario_service import UsuarioService
from app.services.producto_service import ProductoService
from app.utils.decorators import admin_required
from app.models.mesa import Mesa
from app.models.comanda import Comanda
from app.models.factura import Factura
from app import db

comanda_bp = Blueprint("comanda", __name__)

# =============================================================================
# RUTAS ADMINISTRADOR
# =============================================================================

@comanda_bp.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    total_comandas = Comanda.query.count()
    facturas_hoy = Factura.query.filter(Factura.fecha >= db.func.current_date()).count()
    
    return render_template("admin/dashboard.html", 
                           total_comandas=total_comandas,
                           facturas_hoy=facturas_hoy)

@comanda_bp.route("/comandas")
@login_required
@admin_required
def comandas_admin():
    """Listado general de comandas solo para administradores"""
    comandas = ComandaService.listar()
    mesas = MesaService.listar()
    meseros = UsuarioService.listar()
    productos = ProductoService.listar()
    
    return render_template("admin/comandas.html", 
                           comandas=comandas, 
                           mesas=mesas, 
                           meseros=meseros, 
                           productos=productos)

@comanda_bp.route("/comandas/nueva")
@login_required
@admin_required
def nueva_comanda_admin():
    """Formulario de creación desde panel admin"""
    mesas_disponibles = Mesa.query.filter_by(estado='disponible').all()
    meseros = UsuarioService.listar()
    productos = ProductoService.listar()
    
    if not mesas_disponibles:
        flash("No hay mesas disponibles.", "warning")
        return redirect(url_for('comanda.comandas_admin'))
    
    return render_template("admin/comandas.html", 
                           mesas=mesas_disponibles, 
                           meseros=meseros, 
                           productos=productos)

@comanda_bp.route("/comandas/eliminar/<int:id_comanda>")
@login_required
@admin_required
def eliminar(id_comanda):
    exito, mensaje = ComandaService.eliminar(id_comanda)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("comanda.comandas_admin"))


# =============================================================================
# RUTAS MESERO
# =============================================================================

@comanda_bp.route("/mesero/dashboard")
@login_required
def dashboard_mesero():
    """Panel exclusivo del mesero. Filtra por usuario actual."""
    if current_user.rol.nombre.lower() != 'mesero':
        flash("Acceso restringido a meseros.", "warning")
        return redirect(url_for('auth.login'))
    
    # Solo comandas ACTIVAS del mesero logueado
    comandas_activas = Comanda.query.filter(
        Comanda.id_mesero == current_user.id_usuario,
        Comanda.estado.in_(['pendiente', 'en_cocina', 'listo'])
    ).order_by(Comanda.fecha_creacion.desc()).all()
    
    # Mesas disponibles y productos activos para nueva comanda
    mesas_disponibles = Mesa.query.filter_by(estado='disponible').order_by(Mesa.numero).all()
    productos = ProductoService.listar()
    
    return render_template(
        "mesero/dashboard.html", 
        comandas=comandas_activas,
        mesas=mesas_disponibles,
        productos=productos
    )

@comanda_bp.route("/mesas")
@login_required
def mesas_mesero():
    """Vista simplificada de estado de mesas para meseros"""
    if current_user.rol.nombre.lower() != 'mesero':
        flash("Acceso restringido.", "warning")
        return redirect(url_for('auth.login'))
        
    mesas = Mesa.query.order_by(Mesa.numero).all()
    return render_template("mesero/mesas.html", mesas=mesas)

@comanda_bp.route("/comandas/guardar", methods=["POST"])
@login_required
def guardar_comanda():
    """
    Creación de comanda con patrón PRG (Post/Redirect/Get).
    Elimina doble alerta y asegura redirección correcta por rol.
    """
    id_mesa = request.form.get("id_mesa")
    
    if not id_mesa:
        flash("Selecciona una mesa válida.", "danger")
        return redirect(url_for('comanda.dashboard_mesero'))

    # Procesar lista de productos
    ids_prod = request.form.getlist("id_producto[]")
    cantidades = request.form.getlist("cantidad[]")
    productos = []
    
    for i in range(len(ids_prod)):
        if ids_prod[i] and cantidades[i]:
            try:
                productos.append({
                    "id_producto": int(ids_prod[i]),
                    "cantidad": max(1, int(cantidades[i]))
                })
            except ValueError:
                continue

    if not productos:
        flash("Agrega al menos un producto.", "danger")
        return redirect(url_for('comanda.dashboard_mesero'))

    # Usar current_user.id_usuario directamente (seguro y consistente)
    exito, mensaje = ComandaService.crear(int(id_mesa), current_user.id_usuario, productos)
    flash(mensaje, "success" if exito else "danger")
    
    # Redirección inteligente basada en rol REAL del usuario
    rol_actual = current_user.rol.nombre.lower()
    if rol_actual == 'mesero':
        return redirect(url_for('comanda.dashboard_mesero'))
    elif rol_actual == 'administrador':
        return redirect(url_for('comanda.comandas_admin'))
    else:
        return redirect(url_for('auth.login'))


# =============================================================================
# RUTAS COMPARTIDAS / OPERATIVAS
# =============================================================================

@comanda_bp.route("/comandas/actualizar_estado/<int:id_comanda>", methods=["POST"])
@login_required
def actualizar_estado(id_comanda):
    """Cambio de estado accesible por Mesero y Cocinero"""
    estado = request.form.get("estado")
    exito, mensaje = ComandaService.actualizar_estado(id_comanda, estado)
    flash(mensaje, "success" if exito else "error")
    
    # Retornar al dashboard correspondiente según quien ejecutó la acción
    rol_actual = current_user.rol.nombre.lower()
    if rol_actual == 'cocinero':
        return redirect(url_for('comanda.cocinero_dashboard'))
    else:
        return redirect(url_for('comanda.dashboard_mesero'))

@comanda_bp.route("/cocinero/dashboard")
@login_required
def cocinero_dashboard():
    """Pantalla de producción exclusiva para cocina"""
    if current_user.rol.nombre.lower() != 'cocinero':
        flash("Acceso denegado. Área exclusiva para cocina.", "danger")
        return redirect(url_for('auth.login'))
    
    comandas_cocina = Comanda.query.filter(
        Comanda.estado.in_(['pendiente', 'en_cocina'])
    ).order_by(Comanda.fecha_creacion.asc()).all()
    
    return render_template("cocinero/dashboard.html", 
                           comandas=comandas_cocina)