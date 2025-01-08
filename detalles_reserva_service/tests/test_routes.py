from flask import json


def test_login(client):
    """
    Prueba la ruta de login.
    """
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_create_detalle_reserva(client, init_data):
    """
    Prueba la creación y eliminación de un detalle de reserva.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Crear un detalle de reserva
    detalle_data = {"id_reserva": 13, "id_menu": 1, "cantidad": 2}
    response = client.post(
        "/api/detalles_reserva",
        data=json.dumps(detalle_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Detalle de reserva creado"

    # Eliminar el detalle de reserva creado
    detalle_id = data["data"]["id"]
    delete_response = client.delete(
        f"/api/detalles_reserva/{detalle_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert delete_data["message"] == "Detalle de reserva eliminado"


def test_get_detalles_reserva(client, init_data):
    """
    Prueba obtener detalles de reserva existentes.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Obtener detalles de reserva
    response = client.get(
        "/api/detalles_reserva",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_update_detalle_reserva(client, init_data):
    """
    Prueba la actualización de un detalle de reserva existente.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Crear un detalle de reserva
    detalle_data = {"id_reserva": 13, "id_menu": 1, "cantidad": 2}
    create_response = client.post(
        "/api/detalles_reserva",
        data=json.dumps(detalle_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert create_response.status_code == 201
    detalle_id = create_response.get_json()["data"]["id"]

    # Actualizar el detalle de reserva
    update_data = {"id_reserva": 13, "id_menu": 2, "cantidad": 3}
    update_response = client.put(
        f"/api/detalles_reserva/{detalle_id}",
        data=json.dumps(update_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert update_response.status_code == 200
    update_data_response = update_response.get_json()
    assert update_data_response["message"] == "Detalle de reserva actualizado"

    # Eliminar el detalle de reserva actualizado
    delete_response = client.delete(
        f"/api/detalles_reserva/{detalle_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert delete_data["message"] == "Detalle de reserva eliminado"


def test_get_detalle_reserva_not_found(client):
    """
    Prueba obtener un detalle de reserva inexistente.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Obtener un detalle de reserva inexistente
    response = client.get(
        "/api/detalles_reserva/9999",  # ID inexistente
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Detalle de reserva no encontrado"
