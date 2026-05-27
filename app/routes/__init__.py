from flask import Flask
from .health import health_bp
from .auth import auth_bp
from .posts import posts_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(posts_bp, url_prefix="/api/posts")
