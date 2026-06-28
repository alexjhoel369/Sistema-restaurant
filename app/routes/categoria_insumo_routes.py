from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.categoria_insumo_service import CategoriaInsumoService
from app.utils.decorators import admin_required

categoria_insumo_bp = Blueprint("categoria_insumo", __name__)

@categoria_insumo_bp.route("/categorias-insumos")
@login_required
@admin_required
def categorias():
    categorias = CategoriaInsumoService.listar()
    return render_template("admin/categorias_insumos.html", categorias=categorias, editar=None)

@categoria_insumo_bp.route("/categorias-insumos/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    
    exito, mensaje = CategoriaInsumoService.crear(nombre, descripcion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_insumo.categorias"))

@categoria_insumo_bp.route("/categorias-insumos/editar/<int:id_categoria>")
@login_required
@admin_required
def editar(id_categoria):
    editar = CategoriaInsumoService.obtener(id_categoria)
    if not editar:
        flash("La categoría solicitada no existe.", "error")
        return redirect(url_for("categoria_insumo.categorias"))
    categorias = CategoriaInsumoService.listar()
    return render_template("admin/categorias_insumos.html", categorias=categorias, editar=editar)

@categoria_insumo_bp.route("/categorias-insumos/actualizar/<int:id_categoria>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_categoria):
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = CategoriaInsumoService.actualizar(id_categoria, nombre, descripcion, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_insumo.categorias"))

@categoria_insumo_bp.route("/categorias-insumos/eliminar/<int:id_categoria>")
@login_required
@admin_required
def eliminar(id_categoria):
    exito, mensaje = CategoriaInsumoService.eliminar(id_categoria)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_insumo.categorias"))