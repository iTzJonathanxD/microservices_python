from app.models import Reserva, Cliente
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


def validate_reserva_data(data):
    """
    Valida los datos antes de crear o actualizar una reserva.
    """
    if "fecha_reserva" not in data or not isinstance(data["fecha_reserva"], str):
        return {"error": "La fecha de la reserva es obligatoria y debe ser una cadena (YYYY-MM-DD)."}, 400

    if "id_cliente" not in data or not isinstance(data["id_cliente"], int):
        return {"error": "El ID del cliente es obligatorio y debe ser un número entero."}, 400

    # Validar que el cliente exista
    cliente = Cliente.query.get(data["id_cliente"])
    if not cliente:
        return {"error": "El cliente especificado no existe."}, 404

    return None


def get_all_reservas():
    """
    Obtiene todas las reservas.
    """
    reservas = Reserva.query.all()
    return [
        {
            "id": r.id_reserva,
            "fecha": r.fecha_reserva.strftime("%Y-%m-%d"),
            "id_cliente": r.id_cliente,
            "nombre_cliente": r.cliente.nombre_cliente
        }
        for r in reservas
    ]


def get_reserva_by_id(id_reserva):
    """
    Obtiene una reserva por su ID.
    """
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404

    return {
        "id": reserva.id_reserva,
        "fecha": reserva.fecha_reserva.strftime("%Y-%m-%d"),
        "id_cliente": reserva.id_cliente,
        "nombre_cliente": reserva.cliente.nombre_cliente
    }, 200


def create_reserva(data):
    """
    Crea una nueva reserva después de validar los datos.
    """
    validation_error = validate_reserva_data(data)
    if validation_error:
        return validation_error

    reserva = Reserva(fecha_reserva=data["fecha_reserva"], id_cliente=data["id_cliente"])
    db.session.add(reserva)
    db.session.commit()
    return {
        "message": "Reserva creada",
        "data": {
            "id": reserva.id_reserva,
            "fecha": reserva.fecha_reserva.strftime("%Y-%m-%d"),
            "id_cliente": reserva.id_cliente
        }
    }, 201


def update_reserva(id_reserva, data):
    """
    Actualiza una reserva existente.
    """
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404

    validation_error = validate_reserva_data(data)
    if validation_error:
        return validation_error

    reserva.fecha_reserva = data["fecha_reserva"]
    reserva.id_cliente = data["id_cliente"]
    db.session.commit()
    return {
        "message": "Reserva actualizada",
        "data": {
            "id": reserva.id_reserva,
            "fecha": reserva.fecha_reserva.strftime("%Y-%m-%d"),
            "id_cliente": reserva.id_cliente
        }
    }, 200


def delete_reserva(id_reserva):
    """
    Elimina una reserva por ID.
    """
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404

    reserva_data = {
        "id": reserva.id_reserva,
        "fecha": reserva.fecha_reserva.strftime("%Y-%m-%d"),
        "id_cliente": reserva.id_cliente
    }
    db.session.delete(reserva)
    db.session.commit()
    return {
        "message": "Reserva eliminada",
        "data": reserva_data
    }, 200
