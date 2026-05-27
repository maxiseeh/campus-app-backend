from flask import jsonify, Response
from ..services.health import get_health_status


def health_check() -> Response:
    status = get_health_status()
    return jsonify(status)
