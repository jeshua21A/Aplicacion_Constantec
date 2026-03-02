import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.tables import Base

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")

database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)
    with engine.connect() as connexion:
        logger.info("Conexión exitosa a la base de datos")
except Exception as e:
    logger.warning("Error al conectar la base de datos: ", e)

# Dependencias para obtener sesión de la base de datos
def get_db_factory(session_class):
    def get_db():
        db = session_class()
        try:
            yield db
        finally:
            db.close()
    return get_db

get_db = get_db_factory(SessionLocal)