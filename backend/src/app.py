from flask import Flask, g, jsonify, request
from flask_cors import CORS

import config
from routes.auth_routes import auth_bp
from routes.health_routes import health_bp
from routes.submission_routes import submission_bp
from routes.task_routes import task_bp
from utils.api_error import ApiError

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(submission_bp, url_prefix='/api/submissions')
app.register_blueprint(health_bp, url_prefix='/api/health')


@app.after_request
def add_node_header(response):
    """Equivalente a middlewares/nodeHeaderMiddleware.js: agrega el header
    X-App-Node con fines academicos/demostrativos, para poder comprobar
    que NGINX efectivamente distribuye el trafico entre los tres nodos."""
    response.headers['X-App-Node'] = config.APP_NODE_NAME
    return response


@app.errorhandler(ApiError)
def handle_api_error(err):
    """Equivalente a middlewares/errorMiddleware.js (rama ApiError)."""
    body = {'error': err.message}
    if err.details:
        body['details'] = err.details
    return jsonify(body), err.status_code


@app.errorhandler(404)
def handle_not_found(_err):
    """Equivalente a middlewares/errorMiddleware.js -> notFoundMiddleware."""
    return jsonify({
        'error': f'Ruta no encontrada: {request.method} {request.path}'
    }), 404


@app.errorhandler(Exception)
def handle_unexpected(err):
    """Equivalente a middlewares/errorMiddleware.js (rama generica)."""
    if isinstance(err, ApiError):
        return handle_api_error(err)
    app.logger.exception('[ERROR NO CONTROLADO]')
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
