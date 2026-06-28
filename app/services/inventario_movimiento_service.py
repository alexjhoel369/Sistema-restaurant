from app import db
from app.models.inventario_movimiento import InventarioMovimiento
from app.models.insumo import Insumo
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class InventarioMovimientoService:
    
    @staticmethod
    def listar():
        return InventarioMovimiento.query.order_by(InventarioMovimiento.fecha.desc()).all()

    @staticmethod
    def listar_por_insumo(id_insumo):
        return InventarioMovimiento.query.filter_by(id_insumo=id_insumo).order_by(InventarioMovimiento.fecha.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin):
        return InventarioMovimiento.query.filter(
            InventarioMovimiento.fecha >= fecha_inicio,
            InventarioMovimiento.fecha <= fecha_fin
        ).order_by(InventarioMovimiento.fecha.desc()).all()

    @staticmethod
    def listar_por_tipo(tipo_movimiento):
        return InventarioMovimiento.query.filter_by(tipo_movimiento=tipo_movimiento).order_by(InventarioMovimiento.fecha.desc()).all()

    @staticmethod
    def obtener(id_movimiento):
        return db.session.get(InventarioMovimiento, id_movimiento)

    @staticmethod
    def crear_entrada_compra(id_insumo, cantidad, costo_unitario, id_proveedor, id_usuario, numero_factura=None, motivo=None):
        """Registra una entrada de compra al inventario"""
        return InventarioMovimientoService._crear_movimiento(
            id_insumo=id_insumo,
            tipo_movimiento='entrada_compra',
            cantidad=cantidad,
            costo_unitario=costo_unitario,
            id_proveedor=id_proveedor,
            id_usuario=id_usuario,
            numero_factura=numero_factura,
            motivo=motivo
        )

    @staticmethod
    def crear_salida_merma(id_insumo, cantidad, id_usuario, motivo):
        """Registra una salida por merma o desperdicio"""
        return InventarioMovimientoService._crear_movimiento(
            id_insumo=id_insumo,
            tipo_movimiento='salida_merma',
            cantidad=cantidad,
            costo_unitario=None,
            id_proveedor=None,
            id_usuario=id_usuario,
            motivo=motivo
        )

    @staticmethod
    def crear_ajuste(id_insumo, cantidad, id_usuario, motivo):
        """Registra un ajuste de inventario (positivo=entrada, negativo=salida)"""
        tipo = 'ajuste_entrada' if cantidad > 0 else 'ajuste_salida'
        return InventarioMovimientoService._crear_movimiento(
            id_insumo=id_insumo,
            tipo_movimiento=tipo,
            cantidad=abs(cantidad),
            costo_unitario=None,
            id_proveedor=None,
            id_usuario=id_usuario,
            motivo=motivo
        )

    @staticmethod
    def _crear_movimiento(id_insumo, tipo_movimiento, cantidad, costo_unitario, id_proveedor, id_usuario, numero_factura=None, motivo=None, id_comanda=None):
        """Método interno para crear cualquier tipo de movimiento"""
        if cantidad <= 0:
            return False, "Error: La cantidad debe ser mayor a 0."
        
        try:
            # Validar insumo existente
            insumo = db.session.get(Insumo, id_insumo)
            if not insumo:
                return False, "Error: El insumo no existe."

            # Validar stock suficiente para salidas
            if tipo_movimiento.startswith('salida') or tipo_movimiento.startswith('ajuste_salida'):
                if insumo.stock_actual < cantidad:
                    return False, f"Error: Stock insuficiente. Stock actual: {insumo.stock_actual} {insumo.unidad_medida}"

            # Obtener stock anterior
            stock_anterior = insumo.stock_actual

            # Crear movimiento (el trigger actualizará el stock)
            movimiento = InventarioMovimiento(
                id_insumo=id_insumo,
                tipo_movimiento=tipo_movimiento,
                cantidad=cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=0,  # Se actualizará en el trigger
                costo_unitario=costo_unitario,
                id_proveedor=id_proveedor,
                id_usuario=id_usuario,
                id_comanda=id_comanda,
                numero_factura=numero_factura.strip() if numero_factura else None,
                motivo=motivo.strip() if motivo else None
            )
            db.session.add(movimiento)
            
            # Actualizar costo promedio si es entrada de compra
            if tipo_movimiento == 'entrada_compra' and costo_unitario:
                insumo.costo_unitario_promedio = costo_unitario
            
            db.session.commit()
            return True, "Movimiento de inventario registrado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al registrar movimiento: {str(e)}"

    @staticmethod
    def obtener_kardex(id_insumo, fecha_inicio=None, fecha_fin=None):
        """Obtiene el kardex de un insumo"""
        query = InventarioMovimiento.query.filter_by(id_insumo=id_insumo)
        
        if fecha_inicio:
            query = query.filter(InventarioMovimiento.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(InventarioMovimiento.fecha <= fecha_fin)
        
        return query.order_by(InventarioMovimiento.fecha).all()