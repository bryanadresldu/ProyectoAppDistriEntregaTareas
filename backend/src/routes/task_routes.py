from flask import Blueprint, g, jsonify, request

from services import submission_service, task_service
from utils.decorators import auth_required, role_required
from utils.serializers import serialize_submission, serialize_task

task_bp = Blueprint('tasks', __name__)


# GET /api/tasks -> estudiantes y docentes pueden consultar el listado
# (route('') en vez de route('/') para que la URL final sea exactamente
# "/api/tasks", sin barra final, igual que el router de Express original)
@task_bp.route('', methods=['GET'])
@auth_required
def get_tasks():
    tasks = task_service.list_tasks()
    return jsonify({'tasks': [serialize_task(t) for t in tasks]}), 200


# GET /api/tasks/:id
@task_bp.route('/<int:task_id>', methods=['GET'])
@auth_required
def get_task_by_id(task_id):
    task = task_service.get_task_by_id(task_id)
    return jsonify({'task': serialize_task(task)}), 200


# POST /api/tasks -> SOLO docentes registran tareas nuevas
@task_bp.route('', methods=['POST'])
@auth_required
@role_required('teacher')
def create_task():
    body = request.get_json(silent=True) or {}
    teacher_id = g.user['sub']
    task = task_service.create_task(teacher_id, body)
    return jsonify({
        'message': 'Tarea registrada correctamente',
        'task': serialize_task(task)
    }), 201


# POST /api/tasks/:id/submit -> SOLO estudiantes entregan tareas
@task_bp.route('/<int:task_id>/submit', methods=['POST'])
@auth_required
@role_required('student')
def submit_task(task_id):
    body = request.get_json(silent=True) or {}
    student_id = g.user['sub']
    submission = submission_service.submit_task(student_id, task_id, body.get('answer'))
    return jsonify({
        'message': 'Entrega registrada correctamente',
        'submission': serialize_submission(submission)
    }), 201
