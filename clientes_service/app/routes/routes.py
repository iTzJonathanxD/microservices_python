from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services import (
    validate_login_credentials,
    get_all_clientes,
    get_cliente_by_id,
    create_cliente,
    update_cliente,
    delete_cliente,
)
from app.utils import generate_token, verify_token
from datetime import timedelta

# Blueprints
auth_bp = Blueprint("auth", __name__)
clientes_bp = Blueprint("clientes", __name__)

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


# Ruta para obtener todos los clientes
@clientes_bp.route("/clientes", methods=["GET"])
@verify_token
def get_clientes():
    """
    Devuelve todos los clientes.
    """
    clientes = get_all_clientes()
    return jsonify(clientes), 200


# Ruta para obtener un cliente por ID
@clientes_bp.route("/clientes/<int:id_cliente>", methods=["GET"])
@verify_token
def get_cliente(id_cliente):
    """
    Devuelve un cliente específico por ID.
    """
    cliente, status = get_cliente_by_id(id_cliente)
    return jsonify(cliente), status


# Ruta para crear un cliente
@clientes_bp.route("/clientes", methods=["POST"])
@verify_token
def add_cliente():
    """
    Crea un nuevo cliente.
    """
    data = request.get_json()
    cliente, status = create_cliente(data)
    return jsonify(cliente), status


# Ruta para actualizar un cliente por ID
@clientes_bp.route("/clientes/<int:id_cliente>", methods=["PUT"])
@verify_token
def edit_cliente(id_cliente):
    """
    Actualiza los datos de un cliente existente.
    """
    data = request.get_json()
    cliente, status = update_cliente(id_cliente, data)
    return jsonify(cliente), status


# Ruta para eliminar un cliente por ID
@clientes_bp.route("/clientes/<int:id_cliente>", methods=["DELETE"])
@verify_token
def remove_cliente(id_cliente):
    """
    Elimina un cliente por ID.
    """
    cliente, status = delete_cliente(id_cliente)
    return jsonify(cliente), status
