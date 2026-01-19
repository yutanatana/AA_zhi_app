from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import sys

# 環境変数を取得
env_db_url = "libsql://aa-zhi-db-yutanatana.aws-eu-west-1.turso.io"
auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3Njg2Mjc1NDQsImlkIjoiNTA1MjlkOTYtNmM5ZS00YWJlLTkwMmUtNzVkZDkxNzdlZWNiIiwicmlkIjoiOTBiM2U0YzAtYzJhNC00MTM2LTkwN2QtYjlmN2JlZDQ2MGE0In0.lvFjMzxNRwOJytY3MUt4jybeX-g_m4VHwQArfbmoawKJF8JPb9Ve1GaeqA-BKGR7xfm_mOvbgQS0EoHF_bmNBA"

# 【デバッグログ】
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

if "turso.io" in env_db_url:
    if not auth_token:
        sys.exit("DATABASE_AUTH_TOKEN missing")

    # URLのスキーム（libsql:// または https://）を削除してホスト名だけ抽出
    host = (
        env_db_url
        .replace("libsql://", "")
        .replace("https://", "")
        .replace("sqlite+libsql://", "")
        .split("?")[0]
    )

    print(f"Extracted host: {host}")
    
    # 【修正】connect_argsでトークンを渡す方式に変更
    # トークンをURLに埋め込まず、接続パラメータとして渡す
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{host}"
    
    print(f"Connection URL: {SQLALCHEMY_DATABASE_URL}")
    print(f"Passing auth_token via connect_args")
    print("=" * 50)

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "auth_token": auth_token,
            "secure": True
        },
        poolclass=NullPool,
        echo=False,
    )

else:
    # ローカル開発用
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