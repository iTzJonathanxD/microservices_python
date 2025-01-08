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


def test_login_invalid_credentials(client):
    """
    Prueba la ruta de login con credenciales inválidas.
    """
    response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "wrongpassword"}),
        content_type="application/json",
    )
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Credenciales inválidas"


def test_create_cliente(client):
    """
    Prueba la creación y eliminación de un cliente.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Crear un cliente
    cliente_data = {"nombre_cliente": "Luis Álvarez", "telefono_cliente": "0987654321"}
    response = client.post(
        "/api/clientes",
        data=json.dumps(cliente_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Cliente creado"

    # Eliminar el cliente creado
    cliente_id = data["data"]["id"]
    delete_response = client.delete(
        f"/api/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert delete_data["message"] == "Cliente eliminado"


def test_update_cliente(client):
    """
    Prueba la actualización de un cliente existente y lo elimina después.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Crear un cliente
    cliente_data = {"nombre_cliente": "María Cevallos", "telefono_cliente": "0998765432"}
    create_response = client.post(
        "/api/clientes",
        data=json.dumps(cliente_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert create_response.status_code == 201
    cliente_id = create_response.get_json()["data"]["id"]

    # Actualizar el cliente
    update_data = {"nombre_cliente": "María Fernanda Cevallos", "telefono_cliente": "0991234567"}
    update_response = client.put(
        f"/api/clientes/{cliente_id}",
        data=json.dumps(update_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert update_response.status_code == 200
    update_data_response = update_response.get_json()
    assert update_data_response["message"] == "Cliente actualizado"

    # Eliminar el cliente actualizado
    delete_response = client.delete(
        f"/api/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    delete_data = delete_response.get_json()
    assert delete_data["message"] == "Cliente eliminado"


def test_get_clientes_empty(client):
    """
    Prueba obtener clientes cuando no hay registros.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Hacer solicitud GET a /clientes
    response = client.get(
        "/api/clientes",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0
