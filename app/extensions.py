from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def configure_extensions(app):
    CORS(app)            # Habilita CORS
    db.init_app(app)     # Inicializa o SQLAlchemy
