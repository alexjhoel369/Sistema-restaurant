from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
@admin_required
def dashboard():
    """Dashboard principal del administrador"""
    return render_template("admin/dashboard.html")

@admin_bp.route("/admin/dashboard")
@login_required
@admin_required
def dashboard_redirect():
    return render_template("admin/dashboard.html")