import atexit
import os
from flask import Flask
from app.routes import register_routes
from app.extensions import configure_extensions,db
from app.movie.service import process_csv_to_movies

def create_app(config_class="config.EnvConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configura extensões (SQLAlchemy, CORS, etc.)
    configure_extensions(app)
    
    # Cria todas as tabelas do banco antes de carregar os dados do CSV
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Registra Blueprints/rotas
    register_routes(app)
    
    # Carrega o CSV ao iniciar a aplicação
    # Supondo que o arquivo "data.csv" esteja na raiz do projeto.
    with app.app_context():
        csv_path = os.path.join(app.root_path, "..", "documents/movielist.csv")
        result = process_csv_to_movies(csv_path)
        print(result)  # Exibe o resultado no console
            
    return app
