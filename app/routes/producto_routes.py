from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.producto_service import ProductoService
from app.services.categoria_producto_service import CategoriaProductoService
from app.utils.decorators import admin_required

producto_bp = Blueprint("producto", __name__)

@producto_bp.route("/productos")
@login_required
@admin_required
def productos():
    productos = ProductoService.listar()
    categorias = CategoriaProductoService.listar_activas()
    return render_template("admin/productos.html", productos=productos, categorias=categorias, editar=None)

@producto_bp.route("/productos/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    codigo = request.form.get("codigo")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    precio = request.form.get("precio", type=float)
    id_categoria = request.form.get("id_categoria", type=int)
    tiempo_preparacion = request.form.get("tiempo_preparacion_minutos", type=int, default=15)
    
    exito, mensaje = ProductoService.crear(codigo, nombre, descripcion, precio, id_categoria, tiempo_preparacion)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("producto.productos"))

@producto_bp.route("/productos/editar/<int:id_producto>")
@login_required
@admin_required
def editar(id_producto):
    editar = ProductoService.obtener(id_producto)
    if not editar:
        flash("El producto solicitado no existe.", "error")
        return redirect(url_for("producto.productos"))
    productos = ProductoService.listar()
    categorias = CategoriaProductoService.listar_activas()
    return render_template("admin/productos.html", productos=productos, categorias=categorias, editar=editar)

@producto_bp.route("/productos/actualizar/<int:id_producto>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_producto):
    codigo = request.form.get("codigo")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    precio = request.form.get("precio", type=float)
    id_categoria = request.form.get("id_categoria", type=int)
    tiempo_preparacion = request.form.get("tiempo_preparacion_minutos", type=int, default=15)
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = ProductoService.actualizar(id_producto, codigo, nombre, descripcion, precio, id_categoria, tiempo_preparacion, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("producto.productos"))

@producto_bp.route("/productos/eliminar/<int:id_producto>")
@login_required
@admin_required
def eliminar(id_producto):
    exito, mensaje = ProductoService.eliminar(id_producto)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("producto.productos"))