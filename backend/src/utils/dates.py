from datetime import datetime, timezone

# =============================================================
# Estas funciones existen porque Node y Python manejan fechas de forma
# distinta, pero el CONTRATO con el frontend (que no se toca) debe
# seguir siendo identico al que ya tenia el backend Node:
#
#   - Al RECIBIR una fecha del frontend: llega como ISO 8601 con
#     sufijo "Z" (ej. "2026-07-25T10:00:00.000Z"), generado por
#     `new Date(valorLocal).toISOString()` en el navegador.
#   - Al DEVOLVER una fecha en las respuestas JSON: el frontend espera
#     el mismo formato de string "crudo" que MySQL usa para DATETIME,
#     es decir "YYYY-MM-DD HH:MM:SS" (con espacio, sin "T" ni "Z") --
#     exactamente lo que el driver mysql2 de Node devolvia con
#     `dateStrings: true`. El propio frontend le agrega la "Z" despues
#     (ver frontend/js/tasks.js y teacher.js) antes de mostrarlo en la
#     hora local del usuario.
#
# El servidor MySQL esta configurado en UTC explicito
# (default-time-zone='+00:00'), asi que mysql-connector-python siempre
# entrega/recibe datetimes "naive" (sin tzinfo) que representan un
# instante UTC.
# =============================================================


def parse_iso_utc(value: str) -> datetime:
    """Parsea un string ISO 8601 (con o sin sufijo 'Z') recibido del
    frontend y devuelve un datetime "naive" en UTC, listo para guardarse
    en una columna DATETIME de MySQL."""
    normalized = value.replace('Z', '+00:00')
    parsed = datetime.fromisoformat(normalized)

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

    return parsed


def format_deadline(value) -> str:
    """Convierte un datetime devuelto por MySQL (naive UTC) al mismo
    formato de string plano que el frontend ya sabe interpretar."""
    if value is None:
        return None
    return value.strftime('%Y-%m-%d %H:%M:%S')
