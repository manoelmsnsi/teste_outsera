import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env, se existir
load_dotenv()

class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db" 
class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI", "sqlite:///dev.db")

class ProductionConfig(Config):
    """Configuração para produção"""
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI", "sqlite:///prod.db")

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI", "sqlite:///test.db")

if os.getenv("FLASK_ENV") == "production":
    EnvConfig = ProductionConfig
elif os.getenv("FLASK_ENV") == "testing":
    EnvConfig = TestingConfig
else:
    EnvConfig = DevelopmentConfig