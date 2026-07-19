from db import get_connection


def find_by_email(email):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, nombre_completo AS full_name, correo AS email, '
            'contrasena_hash AS password_hash, rol AS role '
            'FROM usuarios WHERE correo = %s LIMIT 1',
            (email,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    finally:
        conn.close()


def find_by_id(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, nombre_completo AS full_name, correo AS email, rol AS role '
            'FROM usuarios WHERE id = %s LIMIT 1',
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    finally:
        conn.close()
