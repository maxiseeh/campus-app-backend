from flask import Blueprint
from ..controllers.posts import (
    list_posts,
    get_post_stats,
    get_recent_posts,
    get_post,
    create_post,
    delete_post,
)

posts_bp = Blueprint("posts", __name__)
posts_bp.url_map = None  

posts_bp.get("/stats")(get_post_stats)
posts_bp.get("/recent")(get_recent_posts)
posts_bp.get("", strict_slashes=False)(list_posts)
posts_bp.post("", strict_slashes=False)(create_post)
posts_bp.get("/<int:post_id>")(get_post)
posts_bp.delete("/<int:post_id>")(delete_post)