from flask import Blueprint, jsonify, request

from services import auth_service

auth_bp = Blueprint('auth', __name__)


# POST /api/auth/login
@auth_bp.route('/login', methods=['POST'])
def login():
    body = request.get_json(silent=True) or {}
    result = auth_service.login(body.get('email'), body.get('password'))
    return jsonify(result), 200
