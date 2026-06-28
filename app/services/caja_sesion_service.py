from app import db
from app.models.caja_sesion import CajaSesion
from app.models.caja_arqueo import CajaArqueo
from app.models.metodo_pago import MetodoPago
from app.models.usuario import Usuario
from datetime import datetime

class CajaSesionService:
    
    @staticmethod
    def listar():
        return CajaSesion.query.order_by(CajaSesion.fecha_apertura.desc()).all()

    @staticmethod
    def listar_abiertas():
        return CajaSesion.query.filter_by(estado='abierta').order_by(CajaSesion.fecha_apertura.desc()).all()

    @staticmethod
    def listar_por_cajero(id_cajero):
        return CajaSesion.query.filter_by(id_cajero=id_cajero).order_by(CajaSesion.fecha_apertura.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin):
        return CajaSesion.query.filter(
            CajaSesion.fecha_apertura >= fecha_inicio,
            CajaSesion.fecha_apertura <= fecha_fin
        ).order_by(CajaSesion.fecha_apertura.desc()).all()

    @staticmethod
    def obtener(id_sesion):
        return db.session.get(CajaSesion, id_sesion)

    @staticmethod
    def obtener_sesion_activa(id_cajero=None):
        """Obtiene la sesión activa de un cajero o la primera sesión abierta"""
        if id_cajero:
            return CajaSesion.query.filter_by(id_cajero=id_cajero, estado='abierta').first()
        return CajaSesion.query.filter_by(estado='abierta').first()

    @staticmethod
    def abrir_sesion(id_cajero, monto_apertura, montos_por_metodo=None, observaciones=None):
        """
        Abre una nueva sesión de caja
        montos_por_metodo: dict {id_metodo: monto_inicial}
        """
        try:
            # Validar que el cajero existe
            cajero = db.session.get(Usuario, id_cajero)
            if not cajero:
                return False, "Error: El cajero no existe."

            # Validar que no tenga sesión abierta
            sesion_activa = CajaSesion.query.filter_by(id_cajero=id_cajero, estado='abierta').first()
            if sesion_activa:
                return False, "Error: El cajero ya tiene una sesión de caja abierta."

            # Validar monto de apertura
            if monto_apertura < 0:
                return False, "Error: El monto de apertura no puede ser negativo."

            # Crear sesión de caja
            sesion = CajaSesion(
                id_cajero=id_cajero,
                monto_apertura=monto_apertura,
                observaciones=observaciones.strip() if observaciones else None
            )
            db.session.add(sesion)
            db.session.flush()  # Para obtener el id_sesion

            # Crear arqueos por método de pago
            if montos_por_metodo:
                for id_metodo, monto_inicial in montos_por_metodo.items():
                    metodo = db.session.get(MetodoPago, id_metodo)
                    if metodo and metodo.activo:
                        arqueo = CajaArqueo(
                            id_sesion=sesion.id_sesion,
                            id_metodo=id_metodo,
                            monto_inicial=monto_inicial
                        )
                        db.session.add(arqueo)

            db.session.commit()
            return True, f"Sesión de caja #{sesion.id_sesion} abierta exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al abrir sesión de caja: {str(e)}"

    @staticmethod
    def cerrar_sesion(id_sesion, monto_cierre, montos_por_metodo=None, observaciones=None):
        """
        Cierra una sesión de caja
        montos_por_metodo: dict {id_metodo: monto_final}
        """
        try:
            sesion = db.session.get(CajaSesion, id_sesion)
            if not sesion:
                return False, "Sesión de caja no encontrada."
            
            if sesion.estado != 'abierta':
                return False, "Error: La sesión de caja ya está cerrada."

            if monto_cierre < 0:
                return False, "Error: El monto de cierre no puede ser negativo."

            # Calcular diferencia
            diferencia = float(monto_cierre) - float(sesion.monto_acumulado or 0)

            # Actualizar sesión
            sesion.fecha_cierre = datetime.now()
            sesion.monto_cierre = monto_cierre
            sesion.diferencia = diferencia
            sesion.estado = 'cerrada'
            
            if observaciones:
                sesion.observaciones = f"{sesion.observaciones or ''} | {observaciones}"

            # Actualizar arqueos
            if montos_por_metodo:
                for id_metodo, monto_final in montos_por_metodo.items():
                    arqueo = CajaArqueo.query.filter_by(id_sesion=id_sesion, id_metodo=id_metodo).first()
                    if arqueo:
                        arqueo.monto_final = monto_final
                        arqueo.diferencia = monto_final - arqueo.monto_esperado if arqueo.monto_esperado else None

            db.session.commit()
            return True, f"Sesión de caja cerrada exitosamente. Diferencia: Bs.{diferencia:.2f}"
        except Exception as e:
            db.session.rollback()
            return False, f"Error al cerrar sesión de caja: {str(e)}"

    @staticmethod
    def actualizar_monto_acumulado(id_sesion, monto):
        """Actualiza el monto acumulado de la sesión"""
        try:
            sesion = db.session.get(CajaSesion, id_sesion)
            if not sesion:
                return False, "Sesión no encontrada."
            
            if sesion.estado != 'abierta':
                return False, "Error: La sesión no está abierta."

            sesion.monto_acumulado += monto
            db.session.commit()
            return True, "Monto acumulado actualizado."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar monto: {str(e)}"