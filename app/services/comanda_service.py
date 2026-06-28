from app import db
from app.models.comanda import Comanda
from app.models.mesa import Mesa
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.detalle_comanda import DetalleComanda
from app.models.turno_mesero import TurnoMesero
from datetime import datetime

class ComandaService:
    
    @staticmethod
    def listar():
        return Comanda.query.order_by(Comanda.fecha_creacion.desc()).all()

    @staticmethod
    def listar_abiertas():
        return Comanda.query.filter_by(estado='abierta').order_by(Comanda.fecha_creacion.desc()).all()

    @staticmethod
    def listar_por_mesa(id_mesa):
        return Comanda.query.filter_by(id_mesa=id_mesa).order_by(Comanda.fecha_creacion.desc()).all()

    @staticmethod
    def listar_por_mesero(id_mesero):
        return Comanda.query.filter_by(id_mesero=id_mesero).order_by(Comanda.fecha_creacion.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin):
        return Comanda.query.filter(
            Comanda.fecha_creacion >= fecha_inicio,
            Comanda.fecha_creacion <= fecha_fin
        ).order_by(Comanda.fecha_creacion.desc()).all()

    @staticmethod
    def obtener(id_comanda):
        return db.session.get(Comanda, id_comanda)

    @staticmethod
    def crear(id_mesa, id_mesero, id_cliente=None, notas=None):
        """Crea una nueva comanda. Inicia turno automáticamente si no existe."""
        try:
            # Validar mesa
            mesa = db.session.get(Mesa, id_mesa)
            if not mesa:
                return False, "Error: La mesa no existe."
            if mesa.estado == 'mantenimiento':
                return False, "Error: La mesa está en mantenimiento."
            if mesa.estado == 'ocupada':
                return False, "Error: La mesa ya está ocupada."

            # Validar mesero
            mesero = db.session.get(Usuario, id_mesero)
            if not mesero:
                return False, "Error: El mesero no existe."

            # BUSCAR O CREAR TURNO AUTOMÁTICAMENTE
            turno_activo = TurnoMesero.query.filter_by(
                id_usuario=id_mesero, 
                estado='activo'
            ).first()
            
            if not turno_activo:
                turno_activo = TurnoMesero(
                    id_usuario=id_mesero,
                    fecha_inicio=datetime.now(),
                    estado='activo'
                )
                db.session.add(turno_activo)
                db.session.flush()

            # Crear comanda
            comanda = Comanda(
                id_mesa=id_mesa,
                id_mesero=id_mesero,
                id_cliente=id_cliente,
                id_turno=turno_activo.id_turno,
                notas=notas.strip() if notas else None
            )
            db.session.add(comanda)
            
            # Cambiar estado de mesa
            mesa.estado = 'ocupada'
            
            db.session.commit()
            return True, f"Comanda #{comanda.id_comanda} creada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear comanda: {str(e)}"

    @staticmethod
    def agregar_producto(id_comanda, id_producto, cantidad, notas=None):
        """Agrega un producto a la comanda"""
        try:
            comanda = db.session.get(Comanda, id_comanda)
            if not comanda:
                return False, "Comanda no encontrada."
            
            if comanda.estado != 'abierta':
                return False, "Error: Solo se pueden modificar comandas abiertas."

            producto = db.session.get(Producto, id_producto)
            if not producto:
                return False, "Producto no encontrado."
            
            if not producto.activo:
                return False, "Error: El producto no está disponible."

            if cantidad <= 0:
                return False, "Error: La cantidad debe ser mayor a 0."

            # Verificar si el producto ya está en la comanda
            detalle_existente = DetalleComanda.query.filter_by(
                id_comanda=id_comanda, 
                id_producto=id_producto,
                estado_preparacion='pendiente'
            ).first()

            if detalle_existente:
                # Actualizar cantidad (subtotal se recalcula en BD)
                detalle_existente.cantidad += cantidad
            else:
                # NO ENVIAR 'subtotal', la BD lo calcula automáticamente (GENERATED ALWAYS)
                detalle = DetalleComanda(
                    id_comanda=id_comanda,
                    id_producto=id_producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    notas=notas.strip() if notas else None
                )
                db.session.add(detalle)

            db.session.commit()
            
            # Refrescar para obtener el subtotal calculado por la BD
            if not detalle_existente:
                db.session.refresh(detalle)
            
            return True, "Producto agregado a la comanda exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al agregar producto: {str(e)}"

    @staticmethod
    def eliminar_producto(id_detalle):
        """Elimina un producto de la comanda"""
        try:
            detalle = db.session.get(DetalleComanda, id_detalle)
            if not detalle:
                return False, "Detalle no encontrado."

            comanda = db.session.get(Comanda, detalle.id_comanda)
            if comanda.estado != 'abierta':
                return False, "Error: Solo se pueden modificar comandas abiertas."

            db.session.delete(detalle)
            db.session.commit()
            return True, "Producto eliminado de la comanda."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar producto: {str(e)}"

    @staticmethod
    def cerrar(id_comanda):
        """Cierra una comanda"""
        try:
            comanda = db.session.get(Comanda, id_comanda)
            if not comanda:
                return False, "Comanda no encontrada."
            
            if comanda.estado != 'abierta':
                return False, "Error: La comanda ya está cerrada o cancelada."

            comanda.fecha_cierre = datetime.now()
            comanda.estado = 'cerrada'
            
            # Liberar mesa
            mesa = db.session.get(Mesa, comanda.id_mesa)
            if mesa:
                mesa.estado = 'disponible'
            
            db.session.commit()
            return True, "Comanda cerrada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cerrar comanda: {str(e)}"

    @staticmethod
    def cancelar(id_comanda, motivo=None):
        """Cancela una comanda"""
        try:
            comanda = db.session.get(Comanda, id_comanda)
            if not comanda:
                return False, "Comanda no encontrada."
            
            if comanda.estado != 'abierta':
                return False, "Error: Solo se pueden cancelar comandas abiertas."

            comanda.estado = 'cancelada'
            comanda.notas = f"{comanda.notas or ''} | Cancelada: {motivo}" if motivo else comanda.notas
            
            # Liberar mesa
            mesa = db.session.get(Mesa, comanda.id_mesa)
            if mesa:
                mesa.estado = 'disponible'
            
            db.session.commit()
            return True, "Comanda cancelada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cancelar comanda: {str(e)}"