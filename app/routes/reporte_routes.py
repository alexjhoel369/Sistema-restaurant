from flask import Blueprint
from app.controllers.reporte_controller import *

reporte_bp = Blueprint(
    'reporte',
    __name__
)

reporte_bp.route(
    '/reportes'
)(panel_reportes)

reporte_bp.route(
    '/reportes/ventas'
)(reporte_ventas)

reporte_bp.route(
    '/reportes/inventario'
)(reporte_inventario)

reporte_bp.route(
    '/reportes/historial'
)(historial_reportes)