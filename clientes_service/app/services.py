from app.models import Cliente
from app.database import db

USERS_DB = {
    "admin": {"password": "admin123"},
}


def validate_login_credentials(username, password):
    """
    Valida las credenciales de inicio de sesión.
    """
    if username in USERS_DB and USERS_DB[username]["password"] == password:
        return True
    return False


def validate_cliente_data(data):
    """
    Valida los datos antes de crear o actualizar un cliente.
    """
    if "nombre_cliente" not in data or not isinstance(data["nombre_cliente"], str):
        return {"error": "El nombre del cliente es obligatorio y debe ser una cadena."}, 400
    if "telefono_cliente" not in data or not isinstance(data["telefono_cliente"], str):
        return {"error": "El teléfono del cliente es obligatorio y debe ser una cadena."}, 400
    return None


def get_all_clientes():
    """
    Obtiene todos los clientes.
    """
    clientes = Cliente.query.all()
    return [{"id": c.id_cliente, "nombre": c.nombre_cliente, "telefono": c.telefono_cliente} for c in clientes]


def get_cliente_by_id(id_cliente):
    """
    Obtiene un cliente por su ID.
    """
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return {"error": "Cliente no encontrado"}, 404
    return {"id": cliente.id_cliente, "nombre": cliente.nombre_cliente, "telefono": cliente.telefono_cliente}, 200


def create_cliente(data):
    """
    Crea un nuevo cliente después de validar los datos.
    """
    validation_error = validate_cliente_data(data)
    if validation_error:
        return validation_error

    cliente = Cliente(nombre_cliente=data["nombre_cliente"], telefono_cliente=data["telefono_cliente"])
    db.session.add(cliente)
    db.session.commit()
    return {
        "message": "Cliente creado",
        "data": {
            "id": cliente.id_cliente,
            "nombre": cliente.nombre_cliente,
            "telefono": cliente.telefono_cliente
        }
    }, 201


def update_cliente(id_cliente, data):
    """
    Actualiza un cliente existente.
    """
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return {"error": "Cliente no encontrado"}, 404

    validation_error = validate_cliente_data(data)
    if validation_error:
        return validation_error

    cliente.nombre_cliente = data["nombre_cliente"]
    cliente.telefono_cliente = data["telefono_cliente"]
    db.session.commit()
    return {
        "message": "Cliente actualizado",
        "data": {
            "id": cliente.id_cliente,
            "nombre": cliente.nombre_cliente,
            "telefono": cliente.telefono_cliente
        }
    }, 200


def delete_cliente(id_cliente):
    """
    Elimina un cliente por ID.
    """
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        return {"error": "Cliente no encontrado"}, 404

    cliente_data = {
        "id": cliente.id_cliente,
        "nombre": cliente.nombre_cliente,
        "telefono": cliente.telefono_cliente
    }
    db.session.delete(cliente)
    db.session.commit()
    return {
        "message": "Cliente eliminado",
        "data": cliente_data
    }, 200
