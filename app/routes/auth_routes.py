from flask import Blueprint
from app.controllers.auth_controller import login, logout, dashboard

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/', methods=['GET', 'POST'])(login)
auth_bp.route('/logout')(logout)

# ruta dasboard
auth_bp.route('/dashboard')(dashboard)