# app/services/inventario_automatico_service.py

from app import db
from app.models.comanda import Comanda
from app.models.detalle_comanda import DetalleComanda
from app.models.receta import Receta          # Tu tabla receta directa
from app.models.insumo import Insumo
from app.models.inventario_movimiento import InventarioMovimiento
from decimal import Decimal

class InventarioAutomaticoService:

    @staticmethod
    def descontar_por_comanda(id_comanda, id_usuario):
        """
        Descuenta insumos basándose en TU estructura de tabla 'receta'.
        Cada fila en receta es un insumo individual del producto.
        """
        comanda = db.session.get(Comanda, id_comanda)
        if not comanda:
            return False, "Comanda no encontrada"

        try:
            # 1. Obtener todos los productos vendidos en esta comanda
            detalles = DetalleComanda.query.filter_by(id_comanda=id_comanda).all()
            
            for detalle in detalles:
                # 2. Buscar TODAS las filas de receta para este producto
                # (Cada fila es un insumo diferente: carne, pan, salsa, etc.)
                recetas_producto = Receta.query.filter_by(
                    id_producto=detalle.id_producto
                ).all()
                
                if not recetas_producto:
                    continue # Producto sin receta definida (ej: bebida embotellada)

                # 3. Descontar cada insumo individualmente
                for r in recetas_producto:
                    cantidad_a_descontar = r.cantidad_requerida * detalle.cantidad
                    
                    insumo = db.session.get(Insumo, r.id_insumo)
                    if insumo:
                        # Validar stock suficiente antes de restar
                        if insumo.stock_actual < Decimal(str(cantidad_a_descontar)):
                            print(f"⚠️ STOCK INSUFICIENTE: {insumo.nombre} "
                                  f"(Disponible: {insumo.stock_actual}, "
                                  f"Requerido: {cantidad_a_descontar})")
                            # Opcional: permitir venta con stock negativo o bloquear
                        
                        # Restar del stock actual
                        insumo.stock_actual -= Decimal(str(cantidad_a_descontar))
                        
                        # Registrar movimiento en Kardex para trazabilidad
                        movimiento = InventarioMovimiento(
                            id_insumo=insumo.id_insumo,
                            tipo='salida_comanda',
                            cantidad=Decimal(str(cantidad_a_descontar)),
                            id_usuario=id_usuario
                            # Nota: tu tabla inventario_movimiento NO tiene id_comanda,
                            # pero podemos usar id_usuario como referencia
                        )
                        db.session.add(movimiento)

            db.session.commit()
            return True, "Inventario actualizado correctamente"
        
        except Exception as e:
            db.session.rollback()
            return False, f"Error al descontar inventario: {str(e)}"