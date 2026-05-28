from flask import Blueprint
from app.controllers.producto_controller import *

producto_bp = Blueprint('producto', __name__)

producto_bp.route('/productos')(listar_productos)
producto_bp.route('/productos/crear', methods=['GET', 'POST'])(crear_producto)
producto_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])(editar_producto)
producto_bp.route('/productos/eliminar/<int:id>')(eliminar_producto)