import pytest
from app.main import create_app
from app.database import db

@pytest.fixture
def app():
    """
    Crea una instancia de la aplicación Flask para las pruebas.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" 
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    # Inicializa la base de datos
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    """
    Devuelve un cliente de pruebas para hacer solicitudes.
    """
    return app.test_client()
