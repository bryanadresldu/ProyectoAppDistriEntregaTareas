from flask import Blueprint, jsonify

import config
from db import get_connection

health_bp = Blueprint('health', __name__)


# GET /api/health -> confirma que el nodo esta vivo y conectado a MySQL Master
@health_bp.route('', methods=['GET'])
def health():
    try:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
            cursor.close()
        finally:
            conn.close()

        return jsonify({
            'status': 'ok',
            'node': config.APP_NODE_NAME,
            'database': 'connected'
        }), 200
    except Exception:
        return jsonify({
            'status': 'error',
            'node': config.APP_NODE_NAME,
            'database': 'disconnected'
        }), 503
