from app.utils.db import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    contraseña_hash = db.Column(db.String(255),nullable=False)
    id_rol = db.Column(db.Integer,db.ForeignKey('rol.id_rol'))
    activo = db.Column(db.Boolean,default=True)
    rol = db.relationship('Rol')