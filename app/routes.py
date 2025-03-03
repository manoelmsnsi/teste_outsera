from flask import Blueprint
from app.movie.controller import movies_bp
from app.health.controller import health_bp

def register_routes(app: Blueprint) -> None:
    """Registra as rotas da aplicação"""
    app.register_blueprint(movies_bp, url_prefix="/api/movies")
    app.register_blueprint(health_bp, url_prefix="/api/health")
