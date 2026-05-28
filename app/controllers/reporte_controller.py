from flask import render_template

from app.models.factura_model import Factura
from app.models.inventario_model import Inventario
from app.models.reporte_model import Reporte

from app.utils.db import db
from sqlalchemy import func


# PANEL REPORTES
def panel_reportes():

    return render_template(
        'reportes/index.html'
    )


# REPORTE VENTAS
def reporte_ventas():

    facturas = Factura.query.all()

    total_ventas = db.session.query(
        func.sum(Factura.total)
    ).scalar()

    # guardar historial
    reporte = Reporte(
        tipo='ventas',
        descripcion='Reporte general de ventas'
    )

    db.session.add(reporte)
    db.session.commit()

    return render_template(
        'reportes/ventas.html',
        facturas=facturas,
        total_ventas=total_ventas
    )


# REPORTE INVENTARIO
def reporte_inventario():

    inventarios = Inventario.query.all()

    reporte = Reporte(
        tipo='inventario',
        descripcion='Reporte general inventario'
    )

    db.session.add(reporte)
    db.session.commit()

    return render_template(
        'reportes/inventario.html',
        inventarios=inventarios
    )


# HISTORIAL
def historial_reportes():

    reportes = Reporte.query.order_by(
        Reporte.fecha_generacion.desc()
    ).all()

    return render_template(
        'reportes/historial.html',
        reportes=reportes
    )