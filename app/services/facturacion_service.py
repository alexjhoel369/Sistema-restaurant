from app.models.factura_model import Factura
from app.models.factura_detalle_model import FacturaDetalle
from app.models.comanda_model import Comanda
from app.utils.db import db
from datetime import datetime


def cerrar_comanda_y_facturar(id_comanda, metodo_pago):
    comanda = Comanda.query.get(id_comanda)

    if not comanda:
        return False, "Comanda no existe"

    if comanda.total <= 0:
        return False, "No se puede facturar comanda vacía"

    # crear factura
    factura = Factura(
        id_comanda=id_comanda,
        fecha=datetime.now(),
        total=comanda.total
    )

    db.session.add(factura)
    db.session.flush()  # para obtener id_factura

    # registrar pago
    pago = FacturaDetalle(
        id_factura=factura.id_factura,
        metodo_pago=metodo_pago,
        monto=comanda.total
    )

    db.session.add(pago)

    # cambiar estado comanda
    comanda.estado = 'cerrada'

    db.session.commit()

    return True, factura.id_factura