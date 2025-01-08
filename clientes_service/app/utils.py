from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request
from functools import wraps
from flask import jsonify

jwt = JWTManager()

def generate_token(identity, expires_delta=None):
    """
    Genera un token JWT.
    """
    return create_access_token(identity=identity, expires_delta=expires_delta)


def verify_token(f):
    """
    Decorador para verificar el token JWT en las rutas protegidas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Token inválido o ausente"}), 401
        return f(*args, **kwargs)
    return decorated_function
