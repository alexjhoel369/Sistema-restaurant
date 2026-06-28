from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    
    # 1. Configuración de Seguridad para Sesiones
    app.secret_key = 'sabor_unico_clave_secreta_super_segura_2026' 
    
    # 2. Inicialización de Extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    login_manager.login_message_category = 'warning'
    login_manager.session_protection = "strong"

    # 3. ✅ USER LOADER - OBLIGATORIO PARA FLASK-LOGIN
    @login_manager.user_loader
    def load_user(user_id):
        """Carga un usuario desde la base de datos por su ID"""
        from app.models.usuario import Usuario
        return db.session.get(Usuario, int(user_id))

    # 4. Carga Global de Modelos (Necesario para UserMixin)
    from app import models

    # 5. Importación de Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.rol_routes import rol_bp
    from app.routes.usuario_routes import usuario_bp
    from app.routes.cliente_routes import cliente_bp
    from app.routes.mesa_routes import mesa_bp
    from app.routes.categoria_producto_routes import categoria_producto_bp
    from app.routes.producto_routes import producto_bp
    from app.routes.proveedor_routes import proveedor_bp
    from app.routes.categoria_insumo_routes import categoria_insumo_bp
    from app.routes.insumo_routes import insumo_bp
    from app.routes.receta_routes import receta_bp
    from app.routes.inventario_routes import inventario_bp
    from app.routes.comanda_routes import comanda_bp
    from app.routes.caja_sesion_routes import caja_bp
    from app.routes.factura_routes import factura_bp
    from app.routes.configuracion_routes import configuracion_bp
    from app.routes.log_routes import log_bp
    from app.routes.mesero_routes import mesero_bp
    from app.routes.cocinero_routes import cocinero_bp
    from app.routes.cajero_routes import cajero_bp
    from app.routes.almacenero_routes import almacenero_bp

    # 6. Registro de Blueprints
    app.register_blueprint(auth_bp)              # Auth (debe ir primero por la ruta /)
    app.register_blueprint(admin_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(mesa_bp)
    app.register_blueprint(categoria_producto_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(categoria_insumo_bp)
    app.register_blueprint(insumo_bp)
    app.register_blueprint(receta_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(comanda_bp)
    app.register_blueprint(caja_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(configuracion_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(mesero_bp)
    app.register_blueprint(cocinero_bp)
    app.register_blueprint(cajero_bp)
    app.register_blueprint(almacenero_bp)
    


    # 7. Variables Globales para Jinja2
    app.jinja_env.globals.update(float=float)

    @app.context_processor
    def inject_user_data():
        """Pasa el usuario y su rol a TODAS las plantillas automáticamente"""
        from flask_login import current_user
        return {
            'current_user': current_user,
            'is_authenticated': current_user.is_authenticated,
            'rol_actual': session.get('rol', None)
        }

    # 8. Manejadores de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # 9. Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app