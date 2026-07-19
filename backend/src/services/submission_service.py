from datetime import datetime

import mysql.connector

from repositories import submission_repository, task_repository
from utils.api_error import ApiError

MYSQL_DUPLICATE_ENTRY = 1062  # ER_DUP_ENTRY


def submit_task(student_id, task_id, answer):
    if not answer or not answer.strip():
        raise ApiError(400, 'La respuesta no puede estar vacia')

    task = task_repository.find_by_id(task_id)
    if not task:
        raise ApiError(404, 'Tarea no encontrada')

    # Regla de negocio: no se puede entregar despues de la fecha limite.
    # task['deadline'] ya llega como datetime "naive" UTC desde MySQL.
    now = datetime.utcnow()
    if now > task['deadline']:
        raise ApiError(409, 'El plazo de entrega para esta tarea ha finalizado')

    # Verificacion a nivel de aplicacion (respuesta rapida y amigable).
    existing = submission_repository.find_by_student_and_task(student_id, task_id)
    if existing:
        raise ApiError(409, 'Ya has realizado una entrega para esta tarea')

    try:
        # La restriccion UNIQUE(student_id, task_id) en la base de datos es
        # la garantia definitiva ante condiciones de carrera entre nodos
        # concurrentes.
        submission_repository.create(student_id, task_id, answer.strip())
    except mysql.connector.errors.IntegrityError as err:
        if err.errno == MYSQL_DUPLICATE_ENTRY:
            raise ApiError(409, 'Ya has realizado una entrega para esta tarea')
        raise

    return submission_repository.find_by_student_and_task(student_id, task_id)


def list_my_submissions(student_id):
    return submission_repository.find_all_by_student(student_id)


def get_submission_for_task(student_id, task_id):
    submission = submission_repository.find_by_student_and_task(student_id, task_id)
    if not submission:
        raise ApiError(404, 'No has realizado una entrega para esta tarea')
    return submission
