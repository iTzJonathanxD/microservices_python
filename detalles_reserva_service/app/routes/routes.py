from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services import (
    validate_login_credentials,
    get_all_detalles_reserva,
    get_detalle_reserva_by_id,
    create_detalle_reserva,
    update_detalle_reserva,
    delete_detalle_reserva,
)
from app.utils import generate_token, verify_token
from datetime import timedelta

# Blueprints
auth_bp = Blueprint("auth", __name__)
detalles_reserva_bp = Blueprint("detalles_reserva", __name__)

# Ruta de login (Autenticación)
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Maneja el inicio de sesión y genera un token JWT.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Validar credenciales
    if not validate_login_credentials(username, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar token JWT
    token = generate_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": token}), 200


# Ruta para obtener todos los detalles de reserva
@detalles_reserva_bp.route("/detalles_reserva", methods=["GET"])
@verify_token
def get_detalles_reserva():
    """
    Devuelve todos los detalles de reserva.
    """
    detalles = get_all_detalles_reserva()
    return jsonify(detalles), 200


# Ruta para obtener un detalle de reserva por ID
@detalles_reserva_bp.route("/detalles_reserva/<int:id_detalle_reserva>", methods=["GET"])
@verify_token
def get_detalle_reserva(id_detalle_reserva):
    """
    Devuelve un detalle de reserva específico por ID.
    """
    detalle, status = get_detalle_reserva_by_id(id_detalle_reserva)
    return jsonify(detalle), status


# Ruta para crear un detalle de reserva
@detalles_reserva_bp.route("/detalles_reserva", methods=["POST"])
@verify_token
def add_detalle_reserva():
    """
    Crea un nuevo detalle de reserva.
    """
    data = request.get_json()
    detalle, status = create_detalle_reserva(data)
    return jsonify(detalle), status


# Ruta para actualizar un detalle de reserva por ID
@detalles_reserva_bp.route("/detalles_reserva/<int:id_detalle_reserva>", methods=["PUT"])
@verify_token
def edit_detalle_reserva(id_detalle_reserva):
    """
    Actualiza los datos de un detalle de reserva existente.
    """
    data = request.get_json()
    detalle, status = update_detalle_reserva(id_detalle_reserva, data)
    return jsonify(detalle), status


# Ruta para eliminar un detalle de reserva por ID
@detalles_reserva_bp.route("/detalles_reserva/<int:id_detalle_reserva>", methods=["DELETE"])
@verify_token
def remove_detalle_reserva(id_detalle_reserva):
    """
    Elimina un detalle de reserva por ID.
    """
    detalle, status = delete_detalle_reserva(id_detalle_reserva)
    return jsonify(detalle), status
