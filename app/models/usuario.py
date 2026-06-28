from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey("rol.id_rol", ondelete="RESTRICT"), nullable=False)
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Relaciones
    rol = db.relationship("Rol", back_populates="usuarios")
    comandas = db.relationship("Comanda", back_populates="mesero", lazy=True)
    sesiones_caja = db.relationship("CajaSesion", back_populates="cajero", lazy=True)
    logs_auditoria = db.relationship("LogAuditoria", back_populates="usuario", lazy=True)
    turnos = db.relationship("TurnoMesero", back_populates="usuario", lazy=True)
    reservas = db.relationship("Reserva", back_populates="usuario", lazy=True)
    movimientos_inventario = db.relationship("InventarioMovimiento", back_populates="usuario", lazy=True)

    def get_id(self):
        """Flask-Login usa este método para identificar al usuario en la sesión"""
        return str(self.id_usuario)

    @property
    def is_active(self):
        """Permite desactivar usuarios sin borrarlos"""
        return self.activo

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"<Usuario {self.email}>"