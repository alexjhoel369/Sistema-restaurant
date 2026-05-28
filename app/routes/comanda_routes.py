from flask import Blueprint
from app.controllers.comanda_controller import *

comanda_bp = Blueprint('comanda', __name__)

comanda_bp.route('/mesas')(listar_mesas)
comanda_bp.route('/crear_comanda/<int:id_mesa>')(crear_comanda)
comanda_bp.route('/comandas/<int:id>')(ver_comanda)
comanda_bp.route('/comandas/<int:id_comanda>/agregar', methods=['POST'])(agregar_producto)