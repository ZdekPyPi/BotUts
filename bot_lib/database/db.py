from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import urllib.parse
from contextlib import contextmanager

# =========================== RPA DB ==========================================
# PWD                     = urllib.parse.quote(BotVault.DB_PWD)
# SQLALCHEMY_DATABASE_URL = f"postgresql://{BotVault.DB_USER}:{PWD}@{BotVault.DB_HOST}/{BotVault.DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"sqlite:///C:\\BotConfigs\\bots.db"

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
