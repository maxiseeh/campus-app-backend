from flask import Flask, jsonify
from .config import Config
from .extensions import cors, db, migrate
from .routes import register_routes


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    cors.init_app(app, supports_credentials=True, origins="*")
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