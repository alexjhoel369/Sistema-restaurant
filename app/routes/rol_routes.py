from flask import Blueprint
from app.controllers.rol_controller import *

rol_bp = Blueprint(
    'rol',
    __name__
)

rol_bp.route(
    '/roles'
)(listar_roles)

rol_bp.route(
    '/roles/crear',
    methods=['GET', 'POST']
)(crear_rol)

rol_bp.route(
    '/roles/editar/<int:id>',
    methods=['GET', 'POST']
)(editar_rol)

rol_bp.route(
    '/roles/eliminar/<int:id>'
)(eliminar_rol)