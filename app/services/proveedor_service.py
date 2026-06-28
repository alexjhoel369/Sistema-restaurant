from app import db
from app.models.proveedor import Proveedor
from sqlalchemy.exc import IntegrityError

class ProveedorService:
    
    @staticmethod
    def listar():
        return Proveedor.query.order_by(Proveedor.nombre).all()

    @staticmethod
    def listar_activos():
        return Proveedor.query.filter_by(activo=True).order_by(Proveedor.nombre).all()

    @staticmethod
    def obtener(id_proveedor):
        return db.session.get(Proveedor, id_proveedor)

    @staticmethod
    def obtener_por_nit(nit_ci):
        return Proveedor.query.filter_by(nit_ci=nit_ci).first()

    @staticmethod
    def buscar(termino):
        """Busca proveedores por nombre, NIT o teléfono"""
        return Proveedor.query.filter(
            db.or_(
                Proveedor.nombre.ilike(f"%{termino}%"),
                Proveedor.nit_ci.ilike(f"%{termino}%"),
                Proveedor.telefono.ilike(f"%{termino}%")
            )
        ).order_by(Proveedor.nombre).all()

    @staticmethod
    def crear(nombre, nit_ci=None, telefono=None, email=None, direccion=None, contacto_nombre=None):
        if not nombre or not nombre.strip():
            return False, "Error: El nombre del proveedor no puede estar vacío."
        
        try:
            # Validar NIT único si se proporciona
            if nit_ci and nit_ci.strip():
                if Proveedor.query.filter_by(nit_ci=nit_ci.strip()).first():
                    return False, "Error: Ya existe un proveedor con ese NIT/CI."

            proveedor = Proveedor(
                nombre=nombre.strip(),
                nit_ci=nit_ci.strip() if nit_ci else None,
                telefono=telefono.strip() if telefono else None,
                email=email.strip().lower() if email else None,
                direccion=direccion.strip() if direccion else None,
                contacto_nombre=contacto_nombre.strip() if contacto_nombre else None
            )
            db.session.add(proveedor)
            db.session.commit()
            return True, "Proveedor creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un proveedor con ese NIT/CI."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear proveedor: {str(e)}"

    @staticmethod
    def actualizar(id_proveedor, nombre, nit_ci=None, telefono=None, email=None, direccion=None, contacto_nombre=None, activo=True):
        try:
            proveedor = db.session.get(Proveedor, id_proveedor)
            if not proveedor:
                return False, "Proveedor no encontrado."

            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."

            # Validar NIT único si cambió
            if nit_ci and nit_ci.strip() and proveedor.nit_ci != nit_ci.strip():
                if Proveedor.query.filter_by(nit_ci=nit_ci.strip()).first():
                    return False, "Error: Ya existe otro proveedor con ese NIT/CI."

            proveedor.nombre = nombre.strip()
            proveedor.nit_ci = nit_ci.strip() if nit_ci else None
            proveedor.telefono = telefono.strip() if telefono else None
            proveedor.email = email.strip().lower() if email else None
            proveedor.direccion = direccion.strip() if direccion else None
            proveedor.contacto_nombre = contacto_nombre.strip() if contacto_nombre else None
            proveedor.activo = activo

            db.session.commit()
            return True, "Proveedor actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro proveedor con ese NIT/CI."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar proveedor: {str(e)}"

    @staticmethod
    def eliminar(id_proveedor):
        try:
            proveedor = db.session.get(Proveedor, id_proveedor)
            if not proveedor:
                return False, "Proveedor no encontrado."

            db.session.delete(proveedor)
            db.session.commit()
            return True, "Proveedor eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el proveedor porque tiene movimientos de inventario asociados."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"