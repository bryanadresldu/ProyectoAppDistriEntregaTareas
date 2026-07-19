from flask import Blueprint, g, jsonify

from services import submission_service
from utils.decorators import auth_required, role_required
from utils.serializers import serialize_submission

submission_bp = Blueprint('submissions', __name__)


# GET /api/submissions
@submission_bp.route('', methods=['GET'])
@auth_required
@role_required('student')
def get_my_submissions():
    student_id = g.user['sub']
    submissions = submission_service.list_my_submissions(student_id)
    return jsonify({'submissions': [serialize_submission(s) for s in submissions]}), 200


# GET /api/submissions/:taskId
@submission_bp.route('/<int:task_id>', methods=['GET'])
@auth_required
@role_required('student')
def get_submission_for_task(task_id):
    student_id = g.user['sub']
    submission = submission_service.get_submission_for_task(student_id, task_id)
    return jsonify({'submission': serialize_submission(submission)}), 200
