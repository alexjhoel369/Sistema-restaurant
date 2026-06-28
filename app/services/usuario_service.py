from app import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

class UsuarioService:
    
    @staticmethod
    def listar():
        return Usuario.query.order_by(Usuario.id_usuario).all()

    @staticmethod
    def listar_activos():
        return Usuario.query.filter_by(activo=True).order_by(Usuario.id_usuario).all()

    @staticmethod
    def obtener(id_usuario):
        return db.session.get(Usuario, id_usuario)

    @staticmethod
    def obtener_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def crear(nombre, apellido, email, password, id_rol, telefono=None):
        try:
            # Validar campos obligatorios
            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."
            if not apellido or not apellido.strip():
                return False, "Error: El apellido no puede estar vacío."
            if not email or not email.strip():
                return False, "Error: El email no puede estar vacío."
            if not password or not password.strip():
                return False, "Error: La contraseña no puede estar vacía."
            
            # Validar si el email ya existe
            if Usuario.query.filter_by(email=email.strip().lower()).first():
                return False, "El correo electrónico ya está registrado."

            # ✅ CORREGIDO: Especificar método de hash
            nuevo_usuario = Usuario(
                nombre=nombre.strip(),
                apellido=apellido.strip(),
                email=email.strip().lower(),
                contraseña_hash=generate_password_hash(password, method='pbkdf2:sha256'),
                id_rol=id_rol,
                telefono=telefono.strip() if telefono else None,
                activo=True
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return True, "Usuario creado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear usuario: {str(e)}"

    @staticmethod
    def actualizar(id_usuario, nombre, apellido, email, id_rol, activo, telefono=None, password=None):
        try:
            usuario = db.session.get(Usuario, id_usuario)
            if not usuario:
                return False, "Usuario no encontrado."

            # Validar campos obligatorios
            if not nombre or not nombre.strip():
                return False, "Error: El nombre no puede estar vacío."
            if not apellido or not apellido.strip():
                return False, "Error: El apellido no puede estar vacío."

            # Validar duplicados de email si cambió
            if usuario.email != email.strip().lower():
                if Usuario.query.filter_by(email=email.strip().lower()).first():
                    return False, "El correo electrónico ya está en uso por otro usuario."

            usuario.nombre = nombre.strip()
            usuario.apellido = apellido.strip()
            usuario.email = email.strip().lower()
            usuario.id_rol = id_rol
            usuario.activo = activo
            usuario.telefono = telefono.strip() if telefono else None

            # Solo actualizar contraseña si se ingresó una nueva
            if password and password.strip():
                # ✅ CORREGIDO: Especificar método de hash
                usuario.contraseña_hash = generate_password_hash(password, method='pbkdf2:sha256')

            db.session.commit()
            return True, "Usuario actualizado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar usuario: {str(e)}"

    @staticmethod
    def cambiar_password(id_usuario, password_actual, password_nuevo):
        """Cambia la contraseña verificando la actual"""
        usuario = db.session.get(Usuario, id_usuario)
        if not usuario:
            return False, "Usuario no encontrado."
        
        # ✅ CORREGIDO: Usar check_password_hash correctamente
        if not check_password_hash(usuario.contraseña_hash, password_actual):
            return False, "La contraseña actual es incorrecta."
        
        if not password_nuevo or len(password_nuevo) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres."
        
        try:
            # ✅ CORREGIDO: Especificar método de hash
            usuario.contraseña_hash = generate_password_hash(password_nuevo, method='pbkdf2:sha256')
            db.session.commit()
            return True, "Contraseña actualizada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cambiar contraseña: {str(e)}"

    @staticmethod
    def eliminar(id_usuario):
        try:
            usuario = db.session.get(Usuario, id_usuario)
            if not usuario:
                return False, "Usuario no encontrado."

            db.session.delete(usuario)
            db.session.commit()
            return True, "Usuario eliminado exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "No se puede eliminar el usuario porque tiene registros asociados (comandas, movimientos, etc.)."
        except Exception as e:
            db.session.rollback()
            return False, f"Error inesperado al eliminar: {str(e)}"