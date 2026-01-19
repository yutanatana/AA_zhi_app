from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

if "turso.io" in env_db_url:
    if not auth_token:
        sys.exit("DATABASE_AUTH_TOKEN missing")

    host = (
        env_db_url
        .replace("libsql://", "")
        .replace("https://", "")
        .split("?")[0]
    )

    SQLALCHEMY_DATABASE_URL = (
        f"libsql://{host}"
        f"?authToken={auth_token}&secure=true"
    )

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

else:
    engine = create_engine(
        "sqlite:///./sql_app.db",
        connect_args={"check_same_thread": False},
        echo=False,
    )

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# Dependency
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
