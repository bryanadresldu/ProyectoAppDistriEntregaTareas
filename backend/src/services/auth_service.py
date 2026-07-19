import bcrypt

from repositories import user_repository
from utils.api_error import ApiError
from utils.jwt_utils import sign_token


def login(email, password):
    if not email or not password:
        raise ApiError(400, 'Email y contrasena son obligatorios')

    user = user_repository.find_by_email(email)
    if not user:
        raise ApiError(401, 'Credenciales invalidas')

    password_matches = bcrypt.checkpw(
        password.encode('utf-8'),
        user['password_hash'].encode('utf-8')
    )
    if not password_matches:
        raise ApiError(401, 'Credenciales invalidas')

    token = sign_token({'sub': user['id'], 'email': user['email'], 'role': user['role']})

    return {
        'token': token,
        'user': {
            'id': user['id'],
            'fullName': user['full_name'],
            'email': user['email'],
            'role': user['role']
        }
    }
