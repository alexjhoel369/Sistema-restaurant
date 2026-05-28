from flask import Blueprint
from app.controllers.proveedor_controller import *

proveedor_bp = Blueprint(
    'proveedor',
    __name__
)

proveedor_bp.route(
    '/proveedores'
)(listar_proveedores)

proveedor_bp.route(
    '/proveedores/crear',
    methods=['GET', 'POST']
)(crear_proveedor)

proveedor_bp.route(
    '/proveedores/editar/<int:id>',
    methods=['GET', 'POST']
)(editar_proveedor)

proveedor_bp.route(
    '/proveedores/eliminar/<int:id>'
)(eliminar_proveedor)