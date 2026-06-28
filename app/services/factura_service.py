from app import db
from app.models.factura import Factura
from app.models.factura_detalle import FacturaDetalle
from app.models.factura_pago import FacturaPago
from app.models.comanda import Comanda
from app.models.detalle_comanda import DetalleComanda
from app.models.caja_sesion import CajaSesion
from app.models.dosificacion import Dosificacion
from app.models.metodo_pago import MetodoPago

# ✅ IMPORTAR LOS SERVICES NECESARIOS
from app.services.dosificacion_service import DosificacionService

from datetime import datetime

class FacturaService:
    
    @staticmethod
    def listar():
        return Factura.query.order_by(Factura.fecha_emision.desc()).all()

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin):
        return Factura.query.filter(
            Factura.fecha_emision >= fecha_inicio,
            Factura.fecha_emision <= fecha_fin
        ).order_by(Factura.fecha_emision.desc()).all()

    @staticmethod
    def listar_por_cliente(nit_ci):
        return Factura.query.filter_by(nit_ci_cliente=nit_ci).order_by(Factura.fecha_emision.desc()).all()

    @staticmethod
    def listar_anuladas():
        return Factura.query.filter_by(estado='anulada').order_by(Factura.fecha_emision.desc()).all()

    @staticmethod
    def obtener(id_factura):
        return db.session.get(Factura, id_factura)

    @staticmethod
    def obtener_por_cuf(cuf):
        return Factura.query.filter_by(cuf=cuf).first()

    @staticmethod
    def obtener_por_numero(nro_factura):
        return Factura.query.filter_by(nro_factura=nro_factura).first()

    @staticmethod
    def crear_desde_comanda(id_comanda, id_sesion, nit_ci_cliente, razon_social_cliente, 
                           id_metodo_pago, monto_pago, referencia=None, descuento_porcentaje=0, descuento_monto=0):
        """
        Crea una factura a partir de una comanda
        Retorna: (éxito, mensaje, factura_opcional)
        """
        try:
            # Validar comanda
            comanda = db.session.get(Comanda, id_comanda)
            if not comanda:
                return False, "Comanda no encontrada.", None
            
            if comanda.estado == 'cancelada':
                return False, "No se puede facturar una comanda cancelada.", None

            # Validar sesión de caja activa
            sesion = db.session.get(CajaSesion, id_sesion)
            if not sesion or sesion.estado != 'abierta':
                return False, "No hay una sesión de caja activa.", None

            # ✅ Obtener dosificación activa (AHORA SÍ ESTÁ DEFINIDO)
            dosificacion = DosificacionService.obtener_dosificacion_activa()
            if not dosificacion:
                return False, "No hay dosificación activa disponible.", None

            # ✅ Obtener siguiente número de factura
            exito, resultado = DosificacionService.obtener_siguiente_numero(dosificacion.id_dosificacion)
            if not exito:
                return False, resultado, None

            nro_factura = resultado

            # Validar método de pago
            metodo_pago = db.session.get(MetodoPago, id_metodo_pago)
            if not metodo_pago or not metodo_pago.activo:
                return False, "Método de pago no válido.", None

            # Generar CUF simple (en producción usar algoritmo SIAT)
            cuf = f"CUF-{nro_factura}-{dosificacion.nro_autorizacion}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calcular total
            subtotal = float(comanda.total)
            descuento_total = float(descuento_monto)
            if descuento_porcentaje > 0:
                descuento_total += subtotal * (float(descuento_porcentaje) / 100)
            total = subtotal - descuento_total
            
            # Crear factura
            factura = Factura(
                id_comanda=id_comanda,
                id_sesion=id_sesion,
                id_dosificacion=dosificacion.id_dosificacion,
                nro_factura=nro_factura,
                nit_ci_cliente=nit_ci_cliente,
                razon_social_cliente=razon_social_cliente,
                subtotal=subtotal,
                descuento_porcentaje=descuento_porcentaje,
                descuento_monto=descuento_monto,
                importe_base_credito_fiscal=subtotal,  # Simplificado
                total=total,
                cuf=cuf,
                cufd=dosificacion.cufd or f"CUFD-{dosificacion.nro_autorizacion}",
                leyenda=f"Factura emitida según normativa SIAT Bolivia"
            )
            db.session.add(factura)
            db.session.flush()  # Para obtener id_factura

            detalles_comanda = DetalleComanda.query.filter_by(id_comanda=id_comanda).all()
            for det in detalles_comanda:
                    if det.estado_preparacion != 'cancelado':
                        precio = float(det.precio_unitario)
                        cant = det.cantidad
                        detalle_factura = FacturaDetalle(
                            id_factura=factura.id_factura,
                            id_producto=det.id_producto,
                            descripcion=det.producto.nombre,
                            cantidad=cant,
                            precio_unitario=precio,
                            subtotal=cant * precio,  # ✅ Calcular manualmente
                            descuento=0.00
                        )
                        db.session.add(detalle_factura)

            # Crear pago
            pago = FacturaPago(
                id_factura=factura.id_factura,
                id_metodo=id_metodo_pago,
                monto=monto_pago,
                referencia=referencia.strip() if referencia else None
            )
            db.session.add(pago)

            # Actualizar monto acumulado en caja
            sesion.monto_acumulado = float(sesion.monto_acumulado or 0) + float(monto_pago)

            # Cerrar comanda automáticamente
            comanda.estado = 'cerrada'
            comanda.fecha_cierre = datetime.now()

            db.session.commit()
            return True, f"Factura #{nro_factura} emitida exitosamente.", factura
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear factura: {str(e)}", None

    @staticmethod
    def anular(id_factura, motivo):
        """Anula una factura"""
        try:
            factura = db.session.get(Factura, id_factura)
            if not factura:
                return False, "Factura no encontrada."
            
            if factura.estado == 'anulada':
                return False, "La factura ya está anulada."

            factura.estado = 'anulada'
            factura.motivo_anulacion = motivo
            factura.fecha_anulacion = datetime.now()
            
            db.session.commit()
            return True, "Factura anulada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al anular factura: {str(e)}"

    @staticmethod
    def agregar_pago(id_factura, id_metodo_pago, monto, referencia=None):
        """Agrega un pago adicional a la factura"""
        try:
            factura = db.session.get(Factura, id_factura)
            if not factura:
                return False, "Factura no encontrada."
            
            if factura.estado == 'anulada':
                return False, "No se pueden agregar pagos a facturas anuladas."

            # Validar que no exceda el total
            total_pagado = sum(float(p.monto) for p in factura.pagos)
            if total_pagado + float(monto) > float(factura.total):
                return False, f"Error: El pago excede el total de la factura (Bs.{factura.total})"

            # Validar método de pago
            metodo_pago = db.session.get(MetodoPago, id_metodo_pago)
            if not metodo_pago or not metodo_pago.activo:
                return False, "Método de pago no válido."

            # Validar referencia si el método lo requiere
            if metodo_pago.requiere_referencia and (not referencia or not referencia.strip()):
                return False, f"Error: El método {metodo_pago.nombre} requiere una referencia."

            pago = FacturaPago(
                id_factura=id_factura,
                id_metodo=id_metodo_pago,
                monto=monto,
                referencia=referencia.strip() if referencia else None
            )
            db.session.add(pago)
            
            # Actualizar monto en caja
            sesion = db.session.get(CajaSesion, factura.id_sesion)
            if sesion and sesion.estado == 'abierta':
                sesion.monto_acumulado = float(sesion.monto_acumulado or 0) + float(monto)
            
            db.session.commit()
            return True, "Pago agregado exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al agregar pago: {str(e)}"

    @staticmethod
    def calcular_totales_del_dia(fecha=None):
        """Calcula totales de facturación del día"""
        if fecha is None:
            fecha = datetime.now().date()
        
        fecha_inicio = datetime.combine(fecha, datetime.min.time())
        fecha_fin = datetime.combine(fecha, datetime.max.time())
        
        facturas = Factura.query.filter(
            Factura.fecha_emision >= fecha_inicio,
            Factura.fecha_emision <= fecha_fin,
            Factura.estado == 'emitida'
        ).all()
        
        total_emitido = sum(float(f.total) for f in facturas)
        cantidad_facturas = len(facturas)
        
        return {
            'fecha': fecha,
            'cantidad_facturas': cantidad_facturas,
            'total_emitido': total_emitido
        }