from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

# 環境変数を取得
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# URLの先頭を正規化（postgres://などが来ても対応できるように）
# Tursoを使う場合は通常 "libsql://" で始まりますが、SQLAlchemyには "sqlite+libsql://" と伝える必要があります
if "turso.io" in env_db_url:
    if not auth_token:
        sys.exit("DATABASE_AUTH_TOKEN missing")

    # URLのスキーム（libsql:// または https://）を削除してホスト名だけ抽出
    host = (
        env_db_url
        .replace("libsql://", "")
        .replace("https://", "")
        .replace("sqlite+libsql://", "") # 念のためこれも削除対象に
        .split("?")[0]
    )

    # 【重要】プロトコルを "sqlite+libsql://" に指定して構築
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{host}?authToken={auth_token}&secure=true"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

else:
    # ローカル開発用（Render以外の環境で動かす場合）
    # ※Renderでこれを使うとデプロイのたびにデータが消えるので注意
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