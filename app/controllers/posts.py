from flask import request, jsonify, session, Response
from ..services.posts import (
    fetch_post_stats,
    fetch_recent_posts,
    fetch_all_posts,
    fetch_post_by_id,
    insert_post,
    remove_post,
)
from ..services.auth import get_user_by_id

VALID_CATEGORIES = {"study_group", "event", "lost_found", "announcement"}


def get_post_stats() -> Response:
    return jsonify(fetch_post_stats())


def get_recent_posts() -> Response:
    return jsonify(fetch_recent_posts())


def list_posts() -> Response:
    category = request.args.get("category")
    search = request.args.get("search")
    return jsonify(fetch_all_posts(category=category, search=search))


def get_post(post_id: int) -> tuple[Response, int] | Response:
    post = fetch_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


def create_post() -> tuple[Response, int] | Response:
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in to create a post"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 401

    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    category = (data.get("category") or "").strip()

    if not title or not category:
        return jsonify({"error": "Title and category are required"}), 400

    if category not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    post = insert_post(user_id, user["username"], data)
    return jsonify(post), 201


def delete_post(post_id: int) -> tuple[Response, int] | Response:
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "You must be logged in"}), 401

    post = remove_post(post_id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    if post["user_id"] != user_id:
        return jsonify({"error": "You can only delete your own posts"}), 403

    return "", 204
