from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.receta_service import RecetaService
from app.services.producto_service import ProductoService
from app.services.insumo_service import InsumoService
from app.utils.decorators import admin_required

receta_bp = Blueprint("receta", __name__)

@receta_bp.route("/recetas")
@login_required
@admin_required
def recetas():
    """Muestra lista de productos para seleccionar y ver su receta"""
    productos = ProductoService.listar_activos()
    return render_template("admin/recetas.html", productos=productos)

@receta_bp.route("/recetas/producto/<int:id_producto>")
@login_required
@admin_required
def ver_receta(id_producto):
    """Muestra la receta de un producto específico"""
    producto = ProductoService.obtener(id_producto)
    if not producto:
        flash("El producto no existe.", "error")
        return redirect(url_for("receta.recetas"))
    
    recetas = RecetaService.listar_por_producto(id_producto)
    insumos = InsumoService.listar_activos()
    return render_template("admin/recetas_producto.html", producto=producto, recetas=recetas, insumos=insumos)

@receta_bp.route("/recetas/agregar/<int:id_producto>", methods=["POST"])
@login_required
@admin_required
def agregar_ingrediente(id_producto):
    id_insumo = request.form.get("id_insumo", type=int)
    cantidad_requerida = request.form.get("cantidad_requerida", type=float)
    unidad_medida = request.form.get("unidad_medida")
    es_opcional = request.form.get("es_opcional") == 'on'
    notas = request.form.get("notas")
    
    exito, mensaje = RecetaService.crear(id_producto, id_insumo, cantidad_requerida, unidad_medida, es_opcional, notas)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("receta.ver_receta", id_producto=id_producto))

@receta_bp.route("/recetas/eliminar/<int:id_receta>")
@login_required
@admin_required
def eliminar_ingrediente(id_receta):
    receta = RecetaService.obtener(id_receta)
    if not receta:
        flash("El ingrediente de la receta no existe.", "error")
        return redirect(url_for("receta.recetas"))
    
    id_producto = receta.id_producto
    exito, mensaje = RecetaService.eliminar(id_receta)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("receta.ver_receta", id_producto=id_producto))