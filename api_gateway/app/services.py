import requests
from flask import request, jsonify
from app.config.settings import MICROSERVICES

def forward_request(service):
    service_url = MICROSERVICES.get(service)
    if not service_url:
        return jsonify({"error": f"Service '{service}' not found."}), 404

    try:
        if request.method == "GET":
            response = requests.get(service_url, params=request.args)
        elif request.method == "POST":
            response = requests.post(service_url, json=request.json)
        elif request.method == "PUT":
            response = requests.put(service_url, json=request.json)
        elif request.method == "DELETE":
            response = requests.delete(service_url)
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 405

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def list_services():
    return jsonify({"available_services": list(MICROSERVICES.keys())}), 200
