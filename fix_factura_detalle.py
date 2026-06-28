# guarda como fix_factura_detalle.py y ejecuta: python fix_factura_detalle.py
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Eliminar GENERATED ALWAYS de subtotal en factura_detalle
        db.session.execute(text("""
            ALTER TABLE factura_detalle 
            ALTER COLUMN subtotal DROP EXPRESSION;
        """))
        db.session.execute(text("""
            ALTER TABLE factura_detalle 
            ALTER COLUMN subtotal SET DEFAULT 0.00;
        """))
        db.session.commit()
        print("✅ Columna subtotal de factura_detalle corregida")
    except Exception as e:
        print(f"La columna ya estaba corregida o error: {e}")
        db.session.rollback()