from flask import render_template, request, redirect

from app.models.rol_model import Rol
from app.utils.db import db


# LISTAR
def listar_roles():

    roles = Rol.query.all()

    return render_template(
        'roles/listar.html',
        roles=roles
    )


# CREAR
def crear_rol():

    if request.method == 'POST':

        rol = Rol(
            nombre=request.form['nombre']
        )

        db.session.add(rol)
        db.session.commit()

        return redirect('/roles')

    return render_template(
        'roles/crear.html'
    )


# EDITAR
def editar_rol(id):

    rol = Rol.query.get(id)

    if request.method == 'POST':

        rol.nombre = request.form['nombre']

        db.session.commit()

        return redirect('/roles')

    return render_template(
        'roles/editar.html',
        rol=rol
    )


# ELIMINAR
def eliminar_rol(id):

    rol = Rol.query.get(id)

    db.session.delete(rol)

    db.session.commit()

    return redirect('/roles')