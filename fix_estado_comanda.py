# guarda como fix_estado_comanda.py y ejecuta
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE comanda DROP CONSTRAINT IF EXISTS chk_estado_comanda"))
        db.session.execute(text("""
            ALTER TABLE comanda ADD CONSTRAINT chk_estado_comanda 
            CHECK (estado IN ('abierta', 'cerrada', 'cancelada', 'facturada'))
        """))
        db.session.commit()
        print("✅ Estados de comanda actualizados")
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()