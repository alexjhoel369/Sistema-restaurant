from flask import Flask
from .config import Config
from .utils.db import db
from sqlalchemy import text
from app.routes.auth_routes import auth_bp
from app.routes.producto_routes import producto_bp
from app.routes.comanda_routes import comanda_bp
from app.routes.factura_routes import factura_bp
from app.routes.inventario_routes import inventario_bp
from app.routes.proveedor_routes import proveedor_bp
from app.routes.reporte_routes import reporte_bp
from app.routes.mesa_routes import mesa_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.rol_routes import rol_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(comanda_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(reporte_bp)
    app.register_blueprint(mesa_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(rol_bp)

    # 🔥 prueba conexión
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Conexión a BD exitosa")
        except Exception as e:
            print("❌ Error de conexión:", e)
    
    #
    return app