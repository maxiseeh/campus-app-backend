from flask import Flask, jsonify
from .config import Config
from .extensions import cors, db, migrate
from .routes import register_routes

def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    cors.init_app(
        app,
        supports_credentials=True,
        origins=[
            "https://campus-board-frontend-psi.vercel.app",
            "https://campus-board-frontend-git-main-ahadi-s-projects1.vercel.app",
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    )

    db.init_app(app)
    migrate.init_app(app, db)
    register_routes(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        code = getattr(e, "code", 500)
        if not isinstance(code, int):
            code = 500
        return jsonify({"error": str(e) or "Internal server error"}), code

    return app