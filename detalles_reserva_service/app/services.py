from app.models import DetalleReserva, Reserva, Menu
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


def validate_detalle_reserva_data(data):
    """
    Valida los datos antes de crear o actualizar un detalle de reserva.
    """
    if "id_reserva" not in data or not isinstance(data["id_reserva"], int):
        return {"error": "El ID de la reserva es obligatorio y debe ser un número."}, 400
    if "id_menu" not in data or not isinstance(data["id_menu"], int):
        return {"error": "El ID del menú es obligatorio y debe ser un número."}, 400
    if "cantidad" not in data or not isinstance(data["cantidad"], int) or data["cantidad"] <= 0:
        return {"error": "La cantidad es obligatoria y debe ser un número positivo."}, 400
    return None


def get_all_detalles_reserva():
    """
    Obtiene todos los detalles de reserva.
    """
    detalles = DetalleReserva.query.all()
    return [
        {
            "id": d.id_detalle_reserva,
            "id_reserva": d.id_reserva,
            "id_menu": d.id_menu,
            "cantidad": d.cantidad,
        }
        for d in detalles
    ]


def get_detalle_reserva_by_id(id_detalle_reserva):
    """
    Obtiene un detalle de reserva por su ID.
    """
    detalle = DetalleReserva.query.get(id_detalle_reserva)
    if not detalle:
        return {"error": "Detalle de reserva no encontrado"}, 404
    return {
        "id": detalle.id_detalle_reserva,
        "id_reserva": detalle.id_reserva,
        "id_menu": detalle.id_menu,
        "cantidad": detalle.cantidad,
    }, 200


def create_detalle_reserva(data):
    """
    Crea un nuevo detalle de reserva después de validar los datos.
    """
    validation_error = validate_detalle_reserva_data(data)
    if validation_error:
        return validation_error

    # Verificar existencia de la reserva
    reserva = Reserva.query.get(data["id_reserva"])
    if not reserva:
        return {"error": "La reserva especificada no existe."}, 404

    # Verificar existencia del menú
    menu = Menu.query.get(data["id_menu"])
    if not menu:
        return {"error": "El menú especificado no existe."}, 404

    detalle = DetalleReserva(
        id_reserva=data["id_reserva"],
        id_menu=data["id_menu"],
        cantidad=data["cantidad"],
    )
    db.session.add(detalle)
    db.session.commit()
    return {
        "message": "Detalle de reserva creado",
        "data": {
            "id": detalle.id_detalle_reserva,
            "id_reserva": detalle.id_reserva,
            "id_menu": detalle.id_menu,
            "cantidad": detalle.cantidad,
        },
    }, 201


def update_detalle_reserva(id_detalle_reserva, data):
    """
    Actualiza un detalle de reserva existente.
    """
    detalle = DetalleReserva.query.get(id_detalle_reserva)
    if not detalle:
        return {"error": "Detalle de reserva no encontrado"}, 404

    validation_error = validate_detalle_reserva_data(data)
    if validation_error:
        return validation_error

    # Verificar existencia de la reserva si se actualiza
    if "id_reserva" in data:
        reserva = Reserva.query.get(data["id_reserva"])
        if not reserva:
            return {"error": "La reserva especificada no existe."}, 404

    # Verificar existencia del menú si se actualiza
    if "id_menu" in data:
        menu = Menu.query.get(data["id_menu"])
        if not menu:
            return {"error": "El menú especificado no existe."}, 404

    detalle.id_reserva = data.get("id_reserva", detalle.id_reserva)
    detalle.id_menu = data.get("id_menu", detalle.id_menu)
    detalle.cantidad = data.get("cantidad", detalle.cantidad)
    db.session.commit()
    return {
        "message": "Detalle de reserva actualizado",
        "data": {
            "id": detalle.id_detalle_reserva,
            "id_reserva": detalle.id_reserva,
            "id_menu": detalle.id_menu,
            "cantidad": detalle.cantidad,
        },
    }, 200


def delete_detalle_reserva(id_detalle_reserva):
    """
    Elimina un detalle de reserva por ID.
    """
    detalle = DetalleReserva.query.get(id_detalle_reserva)
    if not detalle:
        return {"error": "Detalle de reserva no encontrado"}, 404

    detalle_data = {
        "id": detalle.id_detalle_reserva,
        "id_reserva": detalle.id_reserva,
        "id_menu": detalle.id_menu,
        "cantidad": detalle.cantidad,
    }
    db.session.delete(detalle)
    db.session.commit()
    return {
        "message": "Detalle de reserva eliminado",
        "data": detalle_data,
    }, 200
