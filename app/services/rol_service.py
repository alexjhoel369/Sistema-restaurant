from app import db
from app.models.rol import Rol
from sqlalchemy.exc import IntegrityError

class RolService:

    @staticmethod
    def listar():
        return Rol.query.order_by(Rol.id_rol).all()

    @staticmethod
    def obtener(id_rol):
        return db.session.get(Rol, id_rol)

    @staticmethod
    def crear(nombre, descripcion=None):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre del rol no puede estar vacío."
        
        try:
            rol = Rol(
                nombre=nombre.strip().capitalize(),
                descripcion=descripcion.strip() if descripcion else None
            )
            db.session.add(rol)
            db.session.commit()
            return True, "Rol creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un rol con ese nombre."

    @staticmethod
    def actualizar(id_rol, nombre, descripcion=None):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre del rol no puede estar vacío."
            
        rol = db.session.get(Rol, id_rol)
        if not rol:
            return False, "Error: El rol no existe."
        
        try:
            rol.nombre = nombre.strip().capitalize()
            rol.descripcion = descripcion.strip() if descripcion else None
            db.session.commit()
            return True, "Rol actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro rol con ese nombre."

    @staticmethod
    def eliminar(id_rol):
        rol = db.session.get(Rol, id_rol)
        if not rol:
            return False, "Error: El rol no existe."

        try:
            db.session.delete(rol)
            db.session.commit()
            return True, "Rol eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: No se puede eliminar el rol porque tiene usuarios asignados."