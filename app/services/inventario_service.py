from app.models.inventario_model import Inventario
from app.models.inventario_movimiento_model import InventarioMovimiento
from app.utils.db import db
from datetime import datetime


def verificar_stock(id_producto, cantidad):
    inventario = Inventario.query.filter_by(id_producto=id_producto).first()

    if not inventario:
        return False, "Producto sin inventario"

    if inventario.stock_actual < cantidad:
        return False, "Stock insuficiente"

    return True, inventario


def descontar_stock(id_producto, cantidad):
    inventario = Inventario.query.filter_by(id_producto=id_producto).first()

    inventario.stock_actual -= cantidad

    movimiento = InventarioMovimiento(
        id_producto=id_producto,
        tipo='salida',
        cantidad=cantidad,
        fecha=datetime.now()
    )

    db.session.add(movimiento)