# guarda como crear_dosificacion.py y ejecuta: python crear_dosificacion.py
from app import create_app, db
from app.models.dosificacion import Dosificacion
from datetime import date, timedelta

app = create_app()
with app.app_context():
    # Verificar si ya existe
    existente = Dosificacion.query.first()
    if existente:
        print(f"✅ Ya existe una dosificación: Autorización {existente.nro_autorizacion}")
        print(f"   Números: {existente.nro_actual} al {existente.nro_final}")
        print(f"   Vigente hasta: {existente.fecha_limite_emision}")
    else:
        # Crear dosificación de prueba
        dosificacion = Dosificacion(
            nro_autorizacion=100123456789,
            nit_empresa=123456789,
            sucursal=0,
            tipo_factura='factura',
            nro_inicial=1,
            nro_actual=1,
            nro_final=99999,
            llave_dosificacion='ABC123XYZ',
            fecha_limite_emision=date.today() + timedelta(days=365),
            cufd='CUFD-TEST-2026',
            codigo_control='CC-001',
            activo=True
        )
        db.session.add(dosificacion)
        db.session.commit()
        print("✅ Dosificación creada exitosamente")
        print(f"   Autorización: {dosificacion.nro_autorizacion}")
        print(f"   Números: {dosificacion.nro_actual} al {dosificacion.nro_final}")
        print(f"   Vigente hasta: {dosificacion.fecha_limite_emision}")