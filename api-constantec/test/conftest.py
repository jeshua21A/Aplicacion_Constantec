import logging
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from database.connection import get_db
from main import app  # Adjust this to your main file path
from models.factories import EstudiantesFactory
from models.tables import Base

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Use a specific test database name
TEST_POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
TEST_DB_URL = TEST_POSTGRES_URL + "constantec_testing"


def ensure_database_exists():
    # Use sqlalchemy_utils for a clean one-liner
    if not database_exists(TEST_DB_URL):
        create_database(TEST_DB_URL)
        logger.info("La base de datos se ha creado con exito")


ensure_database_exists()

try:
    engine = create_engine(TEST_DB_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with engine.connect() as connexion:
        logger.info("Conexión exitosa a la base de datos")
except Exception as e:
    logger.warning("Error al conectar la base de datos: ", e)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Creates the schema once per test session."""
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session():
    """Provides a fresh database session for each test."""
    connection = engine.connect()
    # transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    yield db

    # db.close()
    # transaction.rollback() # Faster than dropping tables: rolls back changes
    connection.close()


@pytest.fixture(autouse=True)
def set_factory_session(session):
    """
    This fixture runs for every test. It takes the 'testSessionLocal'
    (provided by your session fixture) and gives it to the factory.
    """
    EstudiantesFactory._meta.sqlalchemy_session = session
    yield
    # After the test, we reset it to be safe
    EstudiantesFactory._meta.sqlalchemy_session = None


@pytest.fixture
def client(session):
    """Provides the FastAPI TestClient with the database dependency overridden."""

    def override_get_db():
        try:
            yield session
        finally:
            pass  # Session is handled by the fixture lifecycle

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, base_url="http://localhost:8000") as c:
        yield c

    # Reset the overrides so other tests aren't affected
    app.dependency_overrides.clear()
