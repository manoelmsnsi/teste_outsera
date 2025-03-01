from flask import Blueprint
from app.controllers.movies import movies_bp
from app.controllers.health import health_bp

def register_routes(app: Blueprint) -> None:
    """Registra as rotas da aplicação"""
    app.register_blueprint(movies_bp, url_prefix="/api/movies")
    app.register_blueprint(health_bp, url_prefix="/api/health")
