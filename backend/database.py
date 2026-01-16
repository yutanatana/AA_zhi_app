import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- ローカルパス設定（既存のロジックを維持） ---
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")

# --- 接続先URLの決定 ---
# Renderなどの環境変数から取得
env_db_url = os.getenv("DATABASE_URL")
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "")

if env_db_url and ("libsql://" in env_db_url or "https://" in env_db_url):
    # 1. プロトコル部分を除去してドメイン名だけにする
    # 例: "libsql://db-name.turso.io/" -> "db-name.turso.io"
    clean_host = env_db_url.replace("libsql://", "").replace("https://", "").strip("/")
    
    # 2. SQLAlchemy用のURLを組み立てる
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{clean_host}?auth_token={auth_token}"
else:
    # 環境変数が設定されていない場合はローカルのSQLiteを使用
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# --- エンジンとセッションの作成 ---
# SQLite互換のため check_same_thread はそのままでも動作しますが、
# libsqlドライバ側で適切に処理されます。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
