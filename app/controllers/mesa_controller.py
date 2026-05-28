from flask import render_template, request, redirect

from app.models.mesa_model import Mesa
from app.utils.db import db


# LISTAR
def listar_mesas_crud():

    mesas = Mesa.query.all()

    return render_template(
        'mesas/listar.html',
        mesas=mesas
    )


# CREAR
def crear_mesa():

    if request.method == 'POST':

        mesa = Mesa(
            numero=request.form['numero'],
            capacidad=request.form['capacidad'],
            estado=request.form['estado']
        )

        db.session.add(mesa)
        db.session.commit()

        return redirect('/mesas_crud')

    return render_template(
        'mesas/crear.html'
    )


# EDITAR
def editar_mesa(id):

    mesa = Mesa.query.get(id)

    if request.method == 'POST':

        mesa.numero = request.form['numero']
        mesa.capacidad = request.form['capacidad']
        mesa.estado = request.form['estado']

        db.session.commit()

        return redirect('/mesas_crud')

    return render_template(
        'mesas/editar.html',
        mesa=mesa
    )


# ELIMINAR
def eliminar_mesa(id):

    mesa = Mesa.query.get(id)

    db.session.delete(mesa)

    db.session.commit()

    return redirect('/mesas_crud')