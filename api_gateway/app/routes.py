from flask import Blueprint, request, jsonify
from .services import forward_request, list_services

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/", methods=["GET"])
def get_services():
    return list_services()

@api_blueprint.route("/<service>", methods=["GET", "POST", "PUT", "DELETE"])
def gateway(service):
    return forward_request(service)
