import jwt as pyjwt
from datetime import datetime, timedelta, timezone

import config


def _parse_duration_to_seconds(expr):
    """Convierte expresiones tipo '2h', '30m', '10s', '1d' (mismo formato
    que 'expiresIn' de la libreria jsonwebtoken de Node) a segundos.
    Tambien acepta un numero (de segundos) directamente."""
    if isinstance(expr, (int, float)):
        return int(expr)

    text = str(expr).strip()
    if text.isdigit():
        return int(text)

    unit = text[-1].lower()
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    if unit not in multipliers or len(text) < 2:
        raise ValueError(f'Formato de duracion invalido: {expr}')

    return int(float(text[:-1]) * multipliers[unit])


def sign_token(payload: dict) -> str:
    expires_in_seconds = _parse_duration_to_seconds(config.JWT_EXPIRES_IN)
    to_encode = dict(payload)
    to_encode['exp'] = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)
    return pyjwt.encode(to_encode, config.JWT_SECRET, algorithm='HS256')


def verify_token(token: str) -> dict:
    # Lanza pyjwt.PyJWTError (o subclases como ExpiredSignatureError,
    # InvalidTokenError) si el token es invalido o expiro.
    return pyjwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
