from flask import Blueprint
from app.controllers.mesa_controller import *

mesa_bp = Blueprint('mesa_bp', __name__)


mesa_bp.route(
    '/mesas_crud'
)(listar_mesas_crud)

mesa_bp.route(
    '/mesas/crear',
    methods=['GET', 'POST']
)(crear_mesa)

mesa_bp.route(
    '/mesas/editar/<int:id>',
    methods=['GET', 'POST']
)(editar_mesa)

mesa_bp.route(
    '/mesas/eliminar/<int:id>'
)(eliminar_mesa)