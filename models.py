import atexit
import os

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "Doka7744!")
PG_DB = os.getenv("PG_DB", "flask_neto")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5431)

PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class Advertisements(Base):
    __tablename__ = "advs"

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())

Base.metadata.create_all()