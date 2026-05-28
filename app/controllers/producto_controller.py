from flask import render_template, request, redirect
from app.models.producto_model import Producto
from app.models.categoria_model import CategoriaProducto
from app.utils.db import db


def listar_productos():
    productos = Producto.query.all()
    return render_template('productos/listar.html', productos=productos)


def crear_producto():
    categorias = CategoriaProducto.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        id_categoria = request.form['id_categoria']

        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            id_categoria=id_categoria
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect('/productos')

    return render_template('productos/crear.html', categorias=categorias)


def editar_producto(id):
    producto = Producto.query.get(id)
    categorias = CategoriaProducto.query.all()

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.id_categoria = request.form['id_categoria']

        db.session.commit()

        return redirect('/productos')

    return render_template('productos/editar.html', producto=producto, categorias=categorias)


def eliminar_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()

    return redirect('/productos')