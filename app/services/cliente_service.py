from app import db
from app.models.cliente import Cliente
from sqlalchemy.exc import IntegrityError

class ClienteService:
    
    @staticmethod
    def listar():
        return Cliente.query.order_by(Cliente.razon_social).all()

    @staticmethod
    def listar_activos():
        return Cliente.query.filter_by(activo=True).order_by(Cliente.razon_social).all()

    @staticmethod
    def obtener(id_cliente):
        return db.session.get(Cliente, id_cliente)

    @staticmethod
    def obtener_por_nit(nit_ci):
        return Cliente.query.filter_by(nit_ci=nit_ci).first()

    @staticmethod
    def buscar(termino):
        """Busca clientes por nombre, NIT o teléfono"""
        return Cliente.query.filter(
            db.or_(
                Cliente.razon_social.ilike(f"%{termino}%"),
                Cliente.nit_ci.ilike(f"%{termino}%"),
                Cliente.telefono.ilike(f"%{termino}%")
            )
        ).order_by(Cliente.razon_social).all()

    @staticmethod
    def crear(tipo_documento, nit_ci, razon_social, complemento=None, email=None, telefono=None, direccion=None):
        if not nit_ci or not nit_ci.strip():
            return False, "Error: El NIT/CI no puede estar vacío."
        if not razon_social or not razon_social.strip():
            return False, "Error: La razón social no puede estar vacía."
        
        try:
            # Validar duplicado
            if Cliente.query.filter_by(nit_ci=nit_ci.strip()).first():
                return False, "Error: Ya existe un cliente con ese NIT/CI."
            
            cliente = Cliente(
                tipo_documento=tipo_documento.strip().upper(),
                nit_ci=nit_ci.strip(),
                razon_social=razon_social.strip(),
                complemento=complemento.strip() if complemento else None,
                email=email.strip().lower() if email else None,
                telefono=telefono.strip() if telefono else None,
                direccion=direccion.strip() if direccion else None
            )
            db.session.add(cliente)
            db.session.commit()
            return True, "Cliente creado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe un cliente con ese NIT/CI."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear cliente: {str(e)}"

    @staticmethod
    def actualizar(id_cliente, tipo_documento, nit_ci, razon_social, complemento=None, email=None, telefono=None, direccion=None, activo=True):
        try:
            cliente = db.session.get(Cliente, id_cliente)
            if not cliente:
                return False, "Cliente no encontrado."

            # Validar duplicados de NIT si cambió
            if cliente.nit_ci != nit_ci.strip():
                if Cliente.query.filter_by(nit_ci=nit_ci.strip()).first():
                    return False, "Error: Ya existe otro cliente con ese NIT/CI."

            cliente.tipo_documento = tipo_documento.strip().upper()
            cliente.nit_ci = nit_ci.strip()
            cliente.razon_social = razon_social.strip()
            cliente.complemento = complemento.strip() if complemento else None
            cliente.email = email.strip().lower() if email else None
            cliente.telefono = telefono.strip() if telefono else None
            cliente.direccion = direccion.strip() if direccion else None
            cliente.activo = activo

            db.session.commit()
            return True, "Cliente actualizado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Ya existe otro cliente con ese NIT/CI."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar cliente: {str(e)}"

    @staticmethod
    def eliminar(id_cliente):
        try:
            cliente = db.session.get(Cliente, id_cliente)
            if not cliente:
                return False, "Cliente no encontrado."

            db.session.delete(cliente)
            db.session.commit()
            return True, "Cliente eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el cliente porque tiene reservas o comandas asociadas."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"