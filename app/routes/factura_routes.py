from flask import Blueprint
from app.controllers.factura_controller import *

factura_bp = Blueprint('factura', __name__)

factura_bp.route('/cerrar_comanda/<int:id_comanda>', methods=['GET','POST'])(cerrar_comanda)
factura_bp.route('/factura/<int:id_factura>')(ver_factura)