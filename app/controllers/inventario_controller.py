from flask import render_template, request, redirect

from app.models.inventario_model import Inventario
from app.models.producto_model import Producto
from app.models.proveedor_model import Proveedor
from app.models.inventario_movimiento_model import InventarioMovimiento

from app.utils.db import db


# LISTAR INVENTARIO
def listar_inventario():
    inventarios = Inventario.query.all()

    return render_template(
        'inventario/listar.html',
        inventarios=inventarios
    )


# EDITAR STOCK
def editar_stock(id):

    inventario = Inventario.query.get(id)

    if request.method == 'POST':

        nuevo_stock = int(request.form['stock_actual'])

        inventario.stock_actual = nuevo_stock

        db.session.commit()

        return redirect('/inventario')

    return render_template(
        'inventario/editar.html',
        inventario=inventario
    )


# REGISTRAR ENTRADA
def registrar_entrada():

    productos = Producto.query.all()
    proveedores = Proveedor.query.all()

    if request.method == 'POST':

        id_producto = request.form['id_producto']
        cantidad = int(request.form['cantidad'])
        id_proveedor = request.form['id_proveedor']

        # buscar inventario
        inventario = Inventario.query.filter_by(
            id_producto=id_producto
        ).first()

        # SI NO EXISTE -> CREAR
        if not inventario:

            inventario = Inventario(
                id_producto=id_producto,
                stock_actual=0,
                stock_minimo=5
            )

            db.session.add(inventario)
            db.session.flush()

        # aumentar stock
        inventario.stock_actual += cantidad

        # registrar movimiento
        movimiento = InventarioMovimiento(
            id_producto=id_producto,
            tipo='entrada',
            cantidad=cantidad,
            id_proveedor=id_proveedor
        )

        db.session.add(movimiento)

        db.session.commit()

        return redirect('/inventario')

    return render_template(
        'inventario/entrada.html',
        productos=productos,
        proveedores=proveedores
    )

# VER MOVIMIENTOS
def movimientos():

    movimientos = InventarioMovimiento.query.order_by(
        InventarioMovimiento.fecha.desc()
    ).all()

    return render_template(
        'inventario/movimientos.html',
        movimientos=movimientos
    )