from flask import render_template, request, redirect, session
from app.models.comanda_model import Comanda
from app.models.detalle_comanda_model import DetalleComanda
from app.models.mesa_model import Mesa
from app.models.producto_model import Producto
from app.utils.db import db
from app.services.inventario_service import verificar_stock, descontar_stock

def listar_mesas():
    mesas = Mesa.query.all()
    return render_template('mesas/listar.html', mesas=mesas)


def crear_comanda(id_mesa):
    comanda = Comanda(
        id_mesa=id_mesa,
        id_mesero=session['user_id']
    )

    db.session.add(comanda)
    db.session.commit()

    return redirect(f'/comandas/{comanda.id_comanda}')


def ver_comanda(id):
    comanda = Comanda.query.get(id)
    productos = Producto.query.all()
    detalles = DetalleComanda.query.filter_by(id_comanda=id).all()

    return render_template(
        'comandas/ver.html',
        comanda=comanda,
        productos=productos,
        detalles=detalles
    )


def agregar_producto(id_comanda):
    id_producto = request.form['id_producto']
    cantidad = int(request.form['cantidad'])

    producto = Producto.query.get(id_producto)

    # VALIDAR STOCK
    valido, resultado = verificar_stock(id_producto, cantidad)

    if not valido:
        comanda = Comanda.query.get(id_comanda)
        productos = Producto.query.all()
        detalles = DetalleComanda.query.filter_by(id_comanda=id_comanda).all()

        return render_template(
            'comandas/ver.html',
            comanda=comanda,
            productos=productos,
            detalles=detalles,
            error=resultado
        )

    # CREAR DETALLE
    detalle = DetalleComanda(
        id_comanda=id_comanda,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=producto.precio
    )

    db.session.add(detalle)

    # DESCONTAR STOCK
    descontar_stock(id_producto, cantidad)

    # RECALCULAR TOTAL
    total = 0
    detalles = DetalleComanda.query.filter_by(id_comanda=id_comanda).all()

    for d in detalles:
        total += d.cantidad * d.precio_unitario

    comanda = Comanda.query.get(id_comanda)
    comanda.total = total

    db.session.commit()

    return redirect(f'/comandas/{id_comanda}')