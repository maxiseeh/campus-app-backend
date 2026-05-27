from flask import Blueprint
from ..controllers.health import health_check

health_bp = Blueprint("health", __name__)

health_bp.get("/healthz")(health_check)