from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

# 環境変数を取得
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# 【デバッグログ追加】
print("=" * 50)
print("DEBUG: Database Configuration")
print("=" * 50)
print(f"DATABASE_URL exists: {bool(env_db_url)}")
print(f"DATABASE_URL value: {env_db_url[:50]}..." if env_db_url else "DATABASE_URL value: (empty)")
print(f"AUTH_TOKEN exists: {bool(auth_token)}")
print(f"AUTH_TOKEN length: {len(auth_token)}")
print(f"AUTH_TOKEN starts with 'ey': {auth_token.startswith('ey') if auth_token else False}")
print(f"AUTH_TOKEN first 20 chars: {auth_token[:20]}..." if len(auth_token) > 20 else f"AUTH_TOKEN: {auth_token}")
print("=" * 50)

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

    # 【デバッグログ追加】
    print(f"Extracted host: {host}")
    print(f"Connection URL format: sqlite+libsql://:***@{host}?secure=true")
    print("=" * 50)

    # 【重要】プロトコルを "sqlite+libsql://" に指定して構築
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://:{auth_token}@{host}?secure=true"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

else:
    # ローカル開発用（Render以外の環境で動かす場合）
    # ※Renderでこれを使うとデプロイのたびにデータが消えるので注意
    print("Using local SQLite database")
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