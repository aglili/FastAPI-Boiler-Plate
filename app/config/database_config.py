import os
import signal

import structlog
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

LOG = structlog.get_logger()


engine = create_engine(settings.DB_URI, pool_pre_ping=True)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


try:
    with engine.connect() as conn:
        LOG.info("Pinged The database")
except Exception as e:
    LOG.critical("failed pinging database", error=str(e))
    os.kill(os.getpid(), signal.SIGTERM)


Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(engine)
