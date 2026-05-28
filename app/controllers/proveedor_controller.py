from flask import render_template, request, redirect

from app.models.proveedor_model import Proveedor
from app.utils.db import db


# LISTAR
def listar_proveedores():

    proveedores = Proveedor.query.all()

    return render_template(
        'proveedores/listar.html',
        proveedores=proveedores
    )


# CREAR
def crear_proveedor():

    if request.method == 'POST':

        proveedor = Proveedor(
            nombre=request.form['nombre'],
            telefono=request.form['telefono']
        )

        db.session.add(proveedor)
        db.session.commit()

        return redirect('/proveedores')

    return render_template(
        'proveedores/crear.html'
    )


# EDITAR
def editar_proveedor(id):

    proveedor = Proveedor.query.get(id)

    if request.method == 'POST':

        proveedor.nombre = request.form['nombre']
        proveedor.telefono = request.form['telefono']

        db.session.commit()

        return redirect('/proveedores')

    return render_template(
        'proveedores/editar.html',
        proveedor=proveedor
    )


# ELIMINAR
def eliminar_proveedor(id):

    proveedor = Proveedor.query.get(id)

    db.session.delete(proveedor)

    db.session.commit()

    return redirect('/proveedores')