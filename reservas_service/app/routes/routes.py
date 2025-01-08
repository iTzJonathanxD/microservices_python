from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services import (
    validate_login_credentials,
    get_all_reservas,
    get_reserva_by_id,
    create_reserva,
    update_reserva,
    delete_reserva,
)
from app.utils import generate_token, verify_token
from datetime import timedelta

# Blueprints
auth_bp = Blueprint("auth", __name__)
reservas_bp = Blueprint("reservas", __name__)

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

### Rutas para Reservas
@reservas_bp.route("/reservas", methods=["GET"])
@verify_token
def get_reservas():
    """
    Devuelve todas las reservas.
    """
    reservas = get_all_reservas()
    return jsonify(reservas), 200


@reservas_bp.route("/reservas/<int:id_reserva>", methods=["GET"])
@verify_token
def get_reserva(id_reserva):
    """
    Devuelve una reserva específica por ID.
    """
    reserva, status = get_reserva_by_id(id_reserva)
    return jsonify(reserva), status


@reservas_bp.route("/reservas", methods=["POST"])
@verify_token
def add_reserva():
    """
    Crea una nueva reserva.
    """
    data = request.get_json()
    reserva, status = create_reserva(data)
    return jsonify(reserva), status


@reservas_bp.route("/reservas/<int:id_reserva>", methods=["PUT"])
@verify_token
def edit_reserva(id_reserva):
    """
    Actualiza los datos de una reserva existente.
    """
    data = request.get_json()
    reserva, status = update_reserva(id_reserva, data)
    return jsonify(reserva), status


@reservas_bp.route("/reservas/<int:id_reserva>", methods=["DELETE"])
@verify_token
def remove_reserva(id_reserva):
    """
    Elimina una reserva por ID.
    """
    reserva, status = delete_reserva(id_reserva)
    return jsonify(reserva), status
