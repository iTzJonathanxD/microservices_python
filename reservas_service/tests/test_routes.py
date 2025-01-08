import requests
import json

# URL de la API de clientes
CLIENTES_API_URL = "http://127.0.0.1:8001/api/clientes"

def ensure_cliente_exists(token, nombre, telefono):
    """
    Verifica si el cliente existe en el API REST de clientes, si no lo crea, y retorna su ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(CLIENTES_API_URL, headers=headers)
    assert response.status_code == 200, f"Error al obtener clientes: {response.text}"
    clientes = response.json()

    for cliente in clientes:
        if cliente["nombre"] == nombre and cliente["telefono"] == telefono:
            return cliente["id"]

    # Crear cliente si no existe
    cliente_data = {"nombre_cliente": nombre, "telefono_cliente": telefono}
    response = requests.post(CLIENTES_API_URL, json=cliente_data, headers=headers)
    assert response.status_code == 201, f"Error al crear cliente: {response.text}"
    return response.json()["data"]["id"]


def delete_cliente(token, cliente_id):
    """
    Elimina un cliente en el API REST por su ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{CLIENTES_API_URL}/{cliente_id}", headers=headers)
    assert response.status_code == 200, f"Error al eliminar cliente: {response.text}"


def test_create_reserva_with_cliente(client):
    """
    Prueba la creación de una reserva utilizando el API REST de clientes.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Verificar o crear cliente en el API REST
    cliente_id = ensure_cliente_exists(token, "Luis Álvarez", "0987654321")

    # Crear una reserva
    reserva_data = {"fecha_reserva": "2024-12-15", "id_cliente": cliente_id}
    response = client.post(
        "/api/reservas",
        data=json.dumps(reserva_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert response.status_code == 201
    reserva_id = response.get_json()["data"]["id"]

    # Eliminar la reserva creada
    response = client.delete(
        f"/api/reservas/{reserva_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Eliminar el cliente usado en la prueba
    delete_cliente(token, cliente_id)


def test_get_clientes(client):
    """
    Prueba obtener todos los clientes.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Solicitar todos los clientes
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(CLIENTES_API_URL, headers=headers)
    assert response.status_code == 200, f"Error al obtener clientes: {response.text}"
    clientes = response.json()
    assert isinstance(clientes, list)


def test_update_cliente(client):
    """
    Prueba actualizar un cliente existente.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Verificar o crear cliente en el API REST
    cliente_id = ensure_cliente_exists(token, "Juan Pérez", "0987123456")

    # Actualizar cliente
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"nombre_cliente": "Juan José Pérez", "telefono_cliente": "0998765432"}
    response = requests.put(f"{CLIENTES_API_URL}/{cliente_id}", json=update_data, headers=headers)
    assert response.status_code == 200, f"Error al actualizar cliente: {response.text}"

    # Eliminar el cliente actualizado
    delete_cliente(token, cliente_id)


def test_get_reservas(client, init_data):
    """
    Prueba obtener reservas existentes.
    """
    # Generar un token de prueba
    token_response = client.post(
        "/auth/login",
        data=json.dumps({"username": "admin", "password": "admin123"}),
        content_type="application/json",
    )
    token = token_response.get_json()["access_token"]

    # Crear una reserva
    cliente_id = ensure_cliente_exists(token, "Carla López", "0998765431")
    reserva_data = {"fecha_reserva": "2024-12-20", "id_cliente": cliente_id}
    create_response = client.post(
        "/api/reservas",
        data=json.dumps(reserva_data),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    assert create_response.status_code == 201

    # Obtener reservas
    response = client.get(
        "/api/reservas",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    reservas = response.get_json()
    assert isinstance(reservas, list)
    assert len(reservas) > 0

    # Eliminar la reserva creada
    reserva_id = create_response.get_json()["data"]["id"]
    response = client.delete(
        f"/api/reservas/{reserva_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Eliminar el cliente usado
    delete_cliente(token, cliente_id)
