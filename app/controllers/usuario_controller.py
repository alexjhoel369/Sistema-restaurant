from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash

from app.models.usuario_model import Usuario
from app.models.rol_model import Rol

from app.utils.db import db


# LISTAR
def listar_usuarios():

    usuarios = Usuario.query.all()

    return render_template(
        'usuarios/listar.html',
        usuarios=usuarios
    )


# CREAR
def crear_usuario():

    roles = Rol.query.all()

    if request.method == 'POST':

        password_hash = generate_password_hash(
            request.form['password']
        )

        usuario = Usuario(
            nombre=request.form['nombre'],
            email=request.form['email'],
            contraseña_hash=password_hash,
            id_rol=request.form['id_rol'],
            activo=True
        )

        db.session.add(usuario)
        db.session.commit()

        return redirect('/usuarios')

    return render_template(
        'usuarios/crear.html',
        roles=roles
    )


# EDITAR
def editar_usuario(id):

    usuario = Usuario.query.get(id)

    roles = Rol.query.all()

    if request.method == 'POST':

        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        usuario.id_rol = request.form['id_rol']

        db.session.commit()

        return redirect('/usuarios')

    return render_template(
        'usuarios/editar.html',
        usuario=usuario,
        roles=roles
    )


# ELIMINAR
def eliminar_usuario(id):

    usuario = Usuario.query.get(id)

    db.session.delete(usuario)

    db.session.commit()

    return redirect('/usuarios')