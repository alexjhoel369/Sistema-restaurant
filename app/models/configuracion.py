from app import db

class Configuracion(db.Model):
    __tablename__ = "configuracion"

    id_config = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.String(255))
    tipo = db.Column(db.String(20), default="texto")
    editable = db.Column(db.Boolean, default=True)

    @classmethod
    def obtener_valor(cls, clave, default=None):
        """Obtiene un valor de configuración por su clave"""
        config = cls.query.filter_by(clave=clave).first()
        return config.valor if config else default

    def __repr__(self):
        return f"<Configuracion {self.clave}={self.valor}>"
        