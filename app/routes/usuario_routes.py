from flask import Blueprint
from app.controllers.usuario_controller import *

usuario_bp = Blueprint(
    'usuario',
    __name__
)

usuario_bp.route(
    '/usuarios'
)(listar_usuarios)

usuario_bp.route(
    '/usuarios/crear',
    methods=['GET', 'POST']
)(crear_usuario)

usuario_bp.route(
    '/usuarios/editar/<int:id>',
    methods=['GET', 'POST']
)(editar_usuario)

usuario_bp.route(
    '/usuarios/eliminar/<int:id>'
)(eliminar_usuario)