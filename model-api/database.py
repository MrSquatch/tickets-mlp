"""
Modulo de base de datos para el sistema de clasificacion de tickets.

Maneja la conexion a SQLite y las operaciones basicas de registro
de tickets ya clasificados por el modelo.
"""

import sqlite3
from datetime import datetime, timezone, timedelta

DB_PATH = "tickets.db"

# Zona horaria de Peru/Lima (UTC-5), fija (no tiene horario de verano)
ZONA_HORARIA_LOCAL = timezone(timedelta(hours=-5))

def ahora_local() -> str:
    """Retorna la fecha/hora actual en zona horaria local, formateada como texto."""
    ahora = datetime.now(ZONA_HORARIA_LOCAL)
    return ahora.strftime("%d-%m-%Y %I:%M%p").lower()


def get_connection():
    """Crea y retorna una conexion a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    return conn


def inicializar_db():
    """
    Crea la tabla de tickets si no existe todavia.
    Se debe llamar una vez al iniciar la aplicacion (startup de FastAPI).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_registro TEXT NOT NULL,
            pabellon TEXT NOT NULL,
            laboratorio INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT NOT NULL,
            afectados TEXT NOT NULL,
            comentario TEXT,
            criticidad_predicha TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente'
        )
    """)
    conn.commit()
    conn.close()


def registrar_ticket(ticket_data: dict, prediccion: str) -> int:
    """
    Guarda un ticket ya clasificado en la base de datos.

    Args:
        ticket_data: diccionario con Pabellon, Laboratorio, Categoria,
                     Subcategoria, Afectados, Comentario (opcional)
        prediccion: la criticidad predicha (Baja/Media/Alta)

    Returns:
        El id del ticket recien insertado.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (
            fecha_registro, pabellon, laboratorio, categoria,
            subcategoria, afectados, comentario, criticidad_predicha, estado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ahora_local(),
        ticket_data.get("Pabellon"),
        ticket_data.get("Laboratorio"),
        ticket_data.get("Categoria"),
        ticket_data.get("Subcategoria"),
        ticket_data.get("Afectados"),
        ticket_data.get("Comentario"),
        prediccion,
        "Pendiente"
    ))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id
