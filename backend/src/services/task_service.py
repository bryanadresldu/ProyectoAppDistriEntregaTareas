from datetime import datetime

import mysql.connector

from repositories import task_repository
from utils.api_error import ApiError
from utils.dates import parse_iso_utc

MYSQL_DUPLICATE_ENTRY = 1062  # ER_DUP_ENTRY


def list_tasks():
    return task_repository.find_all()


def get_task_by_id(task_id):
    task = task_repository.find_by_id(task_id)
    if not task:
        raise ApiError(404, 'Tarea no encontrada')
    return task


def create_task(teacher_id, data):
    """Registra una tarea nueva. Solo debe invocarse desde una ruta
    protegida con @role_required('teacher'); este servicio no vuelve a
    validar el rol."""
    data = data or {}
    title = (data.get('title') or '').strip()
    code = (data.get('code') or '').strip()
    description = (data.get('description') or '').strip()
    deadline_raw = data.get('deadline')

    if not title:
        raise ApiError(400, 'El titulo es obligatorio')
    if not code:
        raise ApiError(400, 'El codigo es obligatorio')
    if not description:
        raise ApiError(400, 'La descripcion es obligatoria')
    if not deadline_raw:
        raise ApiError(400, 'La fecha limite es obligatoria')

    try:
        deadline = parse_iso_utc(deadline_raw)
    except (ValueError, TypeError):
        raise ApiError(400, 'La fecha limite no es valida')

    if deadline <= datetime.utcnow():
        raise ApiError(400, 'La fecha limite debe ser posterior al momento actual')

    try:
        return task_repository.create(title, code, description, deadline, teacher_id)
    except mysql.connector.errors.IntegrityError as err:
        if err.errno == MYSQL_DUPLICATE_ENTRY:
            raise ApiError(409, f'Ya existe una tarea con el codigo "{code}"')
        raise
