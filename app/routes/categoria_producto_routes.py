from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.categoria_producto_service import CategoriaProductoService
from app.utils.decorators import admin_required

categoria_producto_bp = Blueprint("categoria_producto", __name__)

@categoria_producto_bp.route("/categorias-productos")
@login_required
@admin_required
def categorias():
    categorias = CategoriaProductoService.listar()
    return render_template("admin/categorias_productos.html", categorias=categorias, editar=None)

@categoria_producto_bp.route("/categorias-productos/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    
    exito, mensaje = CategoriaProductoService.crear(nombre, descripcion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_producto.categorias"))

@categoria_producto_bp.route("/categorias-productos/editar/<int:id_categoria>")
@login_required
@admin_required
def editar(id_categoria):
    editar = CategoriaProductoService.obtener(id_categoria)
    if not editar:
        flash("La categoría solicitada no existe.", "error")
        return redirect(url_for("categoria_producto.categorias"))
    categorias = CategoriaProductoService.listar()
    return render_template("admin/categorias_productos.html", categorias=categorias, editar=editar)

@categoria_producto_bp.route("/categorias-productos/actualizar/<int:id_categoria>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_categoria):
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = CategoriaProductoService.actualizar(id_categoria, nombre, descripcion, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_producto.categorias"))

@categoria_producto_bp.route("/categorias-productos/eliminar/<int:id_categoria>")
@login_required
@admin_required
def eliminar(id_categoria):
    exito, mensaje = CategoriaProductoService.eliminar(id_categoria)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("categoria_producto.categorias"))