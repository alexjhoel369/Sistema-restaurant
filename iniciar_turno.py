from app import create_app, db
from app.models.turno_mesero import TurnoMesero
from app.models.usuario import Usuario
from datetime import datetime

app = create_app()

with app.app_context():
    mesero = Usuario.query.filter_by(id_rol=4).first()
    if mesero:
        turno = TurnoMesero(
            id_usuario=mesero.id_usuario,
            fecha_inicio=datetime.now(),
            estado='activo'
        )
        db.session.add(turno)
        db.session.commit()
        print(f"✅ Turno creado para {mesero.nombre} {mesero.apellido}")
    else:
        print("❌ No hay meseros registrados")