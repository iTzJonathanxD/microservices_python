import pytest
from app.main import create_app
from app.database import db
from app.models import Cliente

@pytest.fixture
def app():
    """
    Configura la aplicación Flask para pruebas con SQLite en memoria.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    """
    Proporciona un cliente de pruebas para la aplicación.
    """
    return app.test_client()

@pytest.fixture
def init_data(app):
    """
    Inicializa datos necesarios para las pruebas.
    """
    with app.app_context():
        db.session.commit()
