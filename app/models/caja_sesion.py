from app import db

class CajaSesion(db.Model):
    __tablename__ = "caja_sesion"

    id_sesion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cajero = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario", ondelete="RESTRICT"), nullable=False)
    fecha_apertura = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    fecha_cierre = db.Column(db.DateTime)
    monto_apertura = db.Column(db.Numeric(10, 2), nullable=False)
    monto_cierre = db.Column(db.Numeric(10, 2))
    monto_acumulado = db.Column(db.Numeric(10, 2), default=0.00)
    diferencia = db.Column(db.Numeric(10, 2))
    estado = db.Column(db.String(15), nullable=False, default="abierta")
    observaciones = db.Column(db.Text)

    # Relaciones
    cajero = db.relationship("Usuario", back_populates="sesiones_caja")
    facturas = db.relationship("Factura", back_populates="sesion_caja", lazy=True)
    arqueos = db.relationship("CajaArqueo", back_populates="sesion", lazy=True)

    @property
    def esta_abierta(self):
        """Verifica si la sesión de caja está abierta"""
        return self.estado == "abierta"

    def cerrar(self, monto_cierre, diferencia):
        """Cierra la sesión de caja"""
        self.fecha_cierre = db.func.current_timestamp()
        self.monto_cierre = monto_cierre
        self.diferencia = diferencia
        self.estado = "cerrada"

    def __repr__(self):
        return f"<CajaSesion {self.id_sesion} - {self.estado}>"