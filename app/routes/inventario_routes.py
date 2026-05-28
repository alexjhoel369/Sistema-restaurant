from flask import Blueprint
from app.controllers.inventario_controller import *

inventario_bp = Blueprint('inventario', __name__)

inventario_bp.route('/inventario')(listar_inventario)

inventario_bp.route(
    '/inventario/editar/<int:id>',
    methods=['GET', 'POST']
)(editar_stock)

inventario_bp.route(
    '/inventario/entrada',
    methods=['GET', 'POST']
)(registrar_entrada)

inventario_bp.route(
    '/inventario/movimientos'
)(movimientos)