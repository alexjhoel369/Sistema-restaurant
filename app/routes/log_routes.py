from flask import Blueprint, render_template, request
from flask_login import login_required
from app.services.log_auditoria_service import LogAuditoriaService
from app.utils.decorators import admin_required

log_bp = Blueprint("log", __name__)

@log_bp.route("/auditoria")
@login_required
@admin_required
def auditoria():
    pagina = request.args.get("pagina", 1, type=int)
    logs = LogAuditoriaService.listar_ultimas_24_horas(limite=500)
    return render_template("admin/auditoria.html", logs=logs)