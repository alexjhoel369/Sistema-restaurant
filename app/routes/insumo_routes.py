from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.insumo_service import InsumoService
from app.services.categoria_insumo_service import CategoriaInsumoService
from app.utils.decorators import admin_required

insumo_bp = Blueprint("insumo", __name__)

@insumo_bp.route("/insumos")
@login_required
@admin_required
def insumos():
    insumos = InsumoService.listar()
    categorias = CategoriaInsumoService.listar_activas()
    return render_template("admin/insumos.html", insumos=insumos, categorias=categorias, editar=None)

@insumo_bp.route("/insumos/guardar", methods=["POST"])
@login_required
@admin_required
def guardar():
    codigo = request.form.get("codigo")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    id_categoria = request.form.get("id_categoria", type=int)
    unidad_medida = request.form.get("unidad_medida")
    stock_minimo = request.form.get("stock_minimo", type=float, default=10)
    stock_maximo = request.form.get("stock_maximo", type=float, default=100)
    costo_unitario = request.form.get("costo_unitario_promedio", type=float, default=0)
    
    exito, mensaje = InsumoService.crear(codigo, nombre, descripcion, id_categoria, unidad_medida, stock_minimo, stock_maximo, costo_unitario)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("insumo.insumos"))

@insumo_bp.route("/insumos/editar/<int:id_insumo>")
@login_required
@admin_required
def editar(id_insumo):
    editar = InsumoService.obtener(id_insumo)
    if not editar:
        flash("El insumo solicitado no existe.", "error")
        return redirect(url_for("insumo.insumos"))
    insumos = InsumoService.listar()
    categorias = CategoriaInsumoService.listar_activas()
    return render_template("admin/insumos.html", insumos=insumos, categorias=categorias, editar=editar)

@insumo_bp.route("/insumos/actualizar/<int:id_insumo>", methods=["POST"])
@login_required
@admin_required
def actualizar(id_insumo):
    codigo = request.form.get("codigo")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    id_categoria = request.form.get("id_categoria", type=int)
    unidad_medida = request.form.get("unidad_medida")
    stock_minimo = request.form.get("stock_minimo", type=float)
    stock_maximo = request.form.get("stock_maximo", type=float)
    costo_unitario = request.form.get("costo_unitario_promedio", type=float)
    activo = request.form.get("activo") == 'on'
    
    exito, mensaje = InsumoService.actualizar(id_insumo, codigo, nombre, descripcion, id_categoria, unidad_medida, stock_minimo, stock_maximo, costo_unitario, activo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("insumo.insumos"))

@insumo_bp.route("/insumos/eliminar/<int:id_insumo>")
@login_required
@admin_required
def eliminar(id_insumo):
    exito, mensaje = InsumoService.eliminar(id_insumo)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("insumo.insumos"))