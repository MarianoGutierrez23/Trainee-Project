
import sqlite3
import os


if not os.path.exists("BD_recepcion.db"):
    db = sqlite3.connect("BD_recepcion.db")
    db_cursor = db.cursor()
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER,
            Elevador TEXT,
            Evento TEXT,
            Equipo TEXT,
            Producción TEXT,
            Fecha_inicio TEXT,
            Día_inicio TEXT,
            Hora_inicio TEXT,
            Minuto_inicio TEXT,
            Fecha_fin TEXT,
            Hora_fin TEXT,
            Minuto_fin TEXT,
            Demora REAL,
            Observaciones TEXT,
            Usuario TEXT,
            PRIMARY KEY(id)

        )
    """)
    db.commit()
    db.close()
    print('Base de Datos creada.')



