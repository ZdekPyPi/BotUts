from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import urllib.parse
from contextlib import contextmanager
import os
# =========================== RPA DB ==========================================
# PWD                     = urllib.parse.quote(BotVault.DB_PWD)
# SQLALCHEMY_DATABASE_URL = f"postgresql://{BotVault.DB_USER}:{PWD}@{BotVault.DB_HOST}/{BotVault.DB_NAME}"
appdata_path = os.getenv('APPDATA')
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    DEFAULT_DB_PATH = os.path.join(appdata_path, "BotConfigs", "bots.db")
    os.makedirs(os.path.dirname(DEFAULT_DB_PATH), exist_ok=True)
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"


rpa_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=280,
    pool_pre_ping=True
)

DbBot = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=rpa_engine))


@contextmanager
def GetDbBot():
    db = DbBot()
    try:
        yield db
    finally:
        db.close()


def create_all():
    from .base import Base
    engine = DbBot().get_bind()
    Base.metadata.create_all(engine)


def mark_iter(seconds):
    pass
