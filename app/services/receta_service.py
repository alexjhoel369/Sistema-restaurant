from app import db
from app.models.receta import Receta
from app.models.producto import Producto
from app.models.insumo import Insumo
from sqlalchemy.exc import IntegrityError

class RecetaService:
    
    @staticmethod
    def listar_por_producto(id_producto):
        return Receta.query.filter_by(id_producto=id_producto).order_by(Receta.id_receta).all()

    @staticmethod
    def listar_por_insumo(id_insumo):
        """Lista todos los productos que usan un insumo específico"""
        return Receta.query.filter_by(id_insumo=id_insumo).all()

    @staticmethod
    def obtener(id_receta):
        return db.session.get(Receta, id_receta)

    @staticmethod
    def crear(id_producto, id_insumo, cantidad_requerida, unidad_medida, es_opcional=False, notas=None):
        if cantidad_requerida <= 0:
            return False, "Error: La cantidad requerida debe ser mayor a 0."
        
        try:
            # Validar producto existente
            producto = db.session.get(Producto, id_producto)
            if not producto:
                return False, "Error: El producto no existe."

            # Validar insumo existente
            insumo = db.session.get(Insumo, id_insumo)
            if not insumo:
                return False, "Error: El insumo no existe."

            # Validar duplicado
            if Receta.query.filter_by(id_producto=id_producto, id_insumo=id_insumo).first():
                return False, "Error: Este insumo ya está asignado a este producto."

            receta = Receta(
                id_producto=id_producto,
                id_insumo=id_insumo,
                cantidad_requerida=cantidad_requerida,
                unidad_medida=unidad_medida,
                es_opcional=es_opcional,
                notas=notas.strip() if notas else None
            )
            db.session.add(receta)
            db.session.commit()
            return True, "Ingrediente agregado a la receta exitosamente."
        except IntegrityError:
            db.session.rollback()
            return False, "Error: Este insumo ya está asignado a este producto."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al agregar ingrediente: {str(e)}"

    @staticmethod
    def actualizar(id_receta, cantidad_requerida, unidad_medida, es_opcional=False, notas=None):
        try:
            receta = db.session.get(Receta, id_receta)
            if not receta:
                return False, "Receta no encontrada."

            if cantidad_requerida <= 0:
                return False, "Error: La cantidad requerida debe ser mayor a 0."

            receta.cantidad_requerida = cantidad_requerida
            receta.unidad_medida = unidad_medida
            receta.es_opcional = es_opcional
            receta.notas = notas.strip() if notas else None

            db.session.commit()
            return True, "Receta actualizada exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al actualizar receta: {str(e)}"

    @staticmethod
    def eliminar(id_receta):
        try:
            receta = db.session.get(Receta, id_receta)
            if not receta:
                return False, "Receta no encontrada."

            db.session.delete(receta)
            db.session.commit()
            return True, "Ingrediente eliminado de la receta exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al eliminar ingrediente: {str(e)}"

    @staticmethod
    def copiar_receta(id_producto_origen, id_producto_destino):
        """Copia todos los ingredientes de un producto a otro"""
        try:
            recetas_origen = Receta.query.filter_by(id_producto=id_producto_origen).all()
            
            if not recetas_origen:
                return False, "El producto origen no tiene receta."

            copiados = 0
            for rec in recetas_origen:
                # Verificar si ya existe el ingrediente en el destino
                if not Receta.query.filter_by(id_producto=id_producto_destino, id_insumo=rec.id_insumo).first():
                    nueva_receta = Receta(
                        id_producto=id_producto_destino,
                        id_insumo=rec.id_insumo,
                        cantidad_requerida=rec.cantidad_requerida,
                        unidad_medida=rec.unidad_medida,
                        es_opcional=rec.es_opcional,
                        notas=rec.notas
                    )
                    db.session.add(nueva_receta)
                    copiados += 1

            db.session.commit()
            return True, f"Se copiaron {copiados} ingredientes exitosamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al copiar receta: {str(e)}"