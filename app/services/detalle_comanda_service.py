from app import db
from app.models.detalle_comanda import DetalleComanda
from app.models.comanda import Comanda

class DetalleComandaService:
    
    @staticmethod
    def listar_por_comanda(id_comanda):
        return DetalleComanda.query.filter_by(id_comanda=id_comanda).order_by(DetalleComanda.id_detalle).all()

    @staticmethod
    def listar_pendientes():
        """Lista detalles pendientes de preparación"""
        return DetalleComanda.query.filter_by(estado_preparacion='pendiente').order_by(DetalleComanda.id_detalle).all()

    @staticmethod
    def listar_en_preparacion():
        return DetalleComanda.query.filter_by(estado_preparacion='en_preparacion').order_by(DetalleComanda.id_detalle).all()

    @staticmethod
    def listar_listos_para_servir():
        return DetalleComanda.query.filter_by(estado_preparacion='listo').order_by(DetalleComanda.id_detalle).all()

    @staticmethod
    def obtener(id_detalle):
        return db.session.get(DetalleComanda, id_detalle)

    @staticmethod
    def cambiar_estado(id_detalle, nuevo_estado):
        """Cambia el estado de preparación de un detalle"""
        estados_validos = ['pendiente', 'en_preparacion', 'listo', 'entregado', 'cancelado']
        
        if nuevo_estado not in estados_validos:
            return False, f"Error: Estado no válido. Debe ser: {', '.join(estados_validos)}"
        
        try:
            detalle = db.session.get(DetalleComanda, id_detalle)
            if not detalle:
                return False, "Detalle no encontrado."

            detalle.estado_preparacion = nuevo_estado
            db.session.commit()
            return True, f"Estado cambiado a '{nuevo_estado}' exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cambiar estado: {str(e)}"

    @staticmethod
    def marcar_como_listo(id_detalle):
        """Marca un detalle como listo para servir (activa el descuento de inventario)"""
        return DetalleComandaService.cambiar_estado(id_detalle, 'listo')

    @staticmethod
    def marcar_como_entregado(id_detalle):
        """Marca un detalle como entregado al cliente"""
        return DetalleComandaService.cambiar_estado(id_detalle, 'entregado')

    @staticmethod
    def cancelar_detalle(id_detalle, motivo=None):
        """Cancela un detalle específico"""
        try:
            detalle = db.session.get(DetalleComanda, id_detalle)
            if not detalle:
                return False, "Detalle no encontrado."

            detalle.estado_preparacion = 'cancelado'
            if motivo:
                detalle.notas = f"{detalle.notas or ''} | Cancelado: {motivo}"
            
            db.session.commit()
            return True, "Detalle cancelado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cancelar detalle: {str(e)}"