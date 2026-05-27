from flask import request, jsonify, session, Response
from ..services.auth import create_user, authenticate_user, get_user_by_id

def signup() -> tuple[Response, int] | Response:
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user = create_user(name, email, password)
    if user is None:
        return jsonify({"error": "Email already in use"}), 400

    session["user_id"] = user["id"]
    return jsonify(user), 201

def login() -> tuple[Response, int] | Response:
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = authenticate_user(email, password)
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]
    return jsonify(user)

def logout() -> Response:
    session.clear()
    return jsonify({"message": "Logged out"})

def me() -> tuple[Response, int] | Response:
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify(user)