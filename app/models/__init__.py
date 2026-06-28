# ===========================================================================
# MÓDULO 1: CONTROL DE ACCESO
# ===========================================================================
from app.models.rol import Rol
from app.models.usuario import Usuario

# ===========================================================================
# MÓDULO 2: CLIENTES
# ===========================================================================
from app.models.cliente import Cliente

# ===========================================================================
# MÓDULO 3: MESAS Y RESERVAS
# ===========================================================================
from app.models.mesa import Mesa
from app.models.reserva import Reserva

# ===========================================================================
# MÓDULO 4: MENÚ Y PLATOS
# ===========================================================================
from app.models.categoria_producto import CategoriaProducto
from app.models.producto import Producto

# ===========================================================================
# MÓDULO 5: INVENTARIO (INSUMOS Y RECETAS)
# ===========================================================================
from app.models.proveedor import Proveedor
from app.models.categoria_insumo import CategoriaInsumo
from app.models.insumo import Insumo
from app.models.receta import Receta
from app.models.inventario_movimiento import InventarioMovimiento

# ===========================================================================
# MÓDULO 6: ATENCIÓN (COMANDAS)
# ===========================================================================
from app.models.turno_mesero import TurnoMesero
from app.models.comanda import Comanda
from app.models.detalle_comanda import DetalleComanda

# ===========================================================================
# MÓDULO 7: CAJA Y PAGOS
# ===========================================================================
from app.models.metodo_pago import MetodoPago
from app.models.caja_sesion import CajaSesion
from app.models.caja_arqueo import CajaArqueo

# ===========================================================================
# MÓDULO 8: FACTURACIÓN (SIAT BOLIVIA)
# ===========================================================================
from app.models.dosificacion import Dosificacion
from app.models.factura import Factura
from app.models.factura_pago import FacturaPago
from app.models.factura_detalle import FacturaDetalle

# ===========================================================================
# MÓDULO 9: CONFIGURACIÓN Y AUDITORÍA
# ===========================================================================
from app.models.configuracion import Configuracion
from app.models.log_auditoria import LogAuditoria