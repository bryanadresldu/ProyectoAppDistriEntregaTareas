from functools import wraps

import jwt as pyjwt
from flask import request, g

from utils.api_error import ApiError
from utils.jwt_utils import verify_token


def auth_required(view_func):
    """Equivalente a middlewares/authMiddleware.js. Exige un header
    'Authorization: Bearer <token>' valido y deja el payload decodificado
    disponible en g.user (equivalente a req.user en Express)."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization', '')

        if not header.startswith('Bearer '):
            raise ApiError(401, 'Token de autenticacion no proporcionado')

        token = header.split(' ', 1)[1]

        try:
            g.user = verify_token(token)
        except pyjwt.PyJWTError:
            raise ApiError(401, 'Token invalido o expirado')

        return view_func(*args, **kwargs)

    return wrapper


def role_required(*allowed_roles):
    """Equivalente a middlewares/roleMiddleware.js (requireRole).
    Debe usarse SIEMPRE despues de @auth_required."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            user = getattr(g, 'user', None)
            if not user or user.get('role') not in allowed_roles:
                raise ApiError(403, 'No tienes permisos para realizar esta accion')
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
