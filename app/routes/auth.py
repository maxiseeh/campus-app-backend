from flask import Blueprint
from ..controllers.auth import signup, login, logout, me

auth_bp = Blueprint("auth", __name__)

auth_bp.post("/signup")(signup)
auth_bp.post("/login")(login)
auth_bp.post("/logout")(logout)
auth_bp.get("/me")(me)
