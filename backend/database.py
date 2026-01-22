from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

if "turso.io" in env_db_url:
    if not auth_token:
        print("Error: DATABASE_AUTH_TOKEN is missing!")
        sys.exit(1)

    # 1. URLのホスト名部分だけをきれいに取り出す
    # (libsql:// xxx.turso.io という形にする)
    host = (
        env_db_url
        .replace("libsql://", "")
        .replace("https://", "")
        .replace("sqlite+libsql://", "")
        .split("?")[0]
    )
    
    # 末尾のスラッシュ削除
    if host.endswith("/"):
        host = host[:-1]

    # 2. 接続URLはシンプルに "sqlite+libsql://ホスト名" だけにする
    # (?secure=true は念のためつけておく)
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{host}?secure=true"
    
    print(f"Connecting to: {SQLALCHEMY_DATABASE_URL}")

    # 3. 【最重要】トークンはここで辞書として渡す
    # これなら記号が含まれていてもURLが壊れません
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"auth_token": auth_token}, # <--- ここがポイント
        poolclass=NullPool,
        echo=False,
    )

else:
    # ローカル開発用
    engine = create_engine(
        "sqlite:///./sql_app.db",
        connect_args={"check_same_thread": False},
        echo=False,
    )

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()