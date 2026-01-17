from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

print(f"--- [DEBUG] DATABASE_URL: {env_db_url}")
print(f"--- [DEBUG] Auth token exists: {bool(auth_token)}")

if "turso.io" in env_db_url:
    print("--- [SETUP] Detected Turso Database ---")

    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing !!!")
        sys.exit(1)

    host = env_db_url.replace("libsql://", "").replace("https://", "").split("?")[0]

    SQLALCHEMY_DATABASE_URL = (
        f"sqlite+libsql://{host}"
        f"?authToken={auth_token}&secure=true"
    )

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
        isolation_level="AUTOCOMMIT",  # ★これが決定打
)


else:
    # ローカル SQLite
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "sql_app.db")

    engine = create_engine(
        f"sqlite:///{DB_PATH}",
        connect_args={"check_same_thread": False},
        echo=False,
    )

# 接続テスト
try:
    print("--- [SETUP] Testing connection...")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("--- [SETUP] Connection OK")
except Exception as e:
    print("!!! CONNECTION ERROR !!!")
    raise

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
