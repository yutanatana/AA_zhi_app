import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 環境変数の取得 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    print(f"--- [SETUP] Detected Turso Database ---")
    
    # 1. トークンの存在チェック
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing !!!")
        sys.exit(1)
    
    # 2. URL から libsql:// 形式に変換
    # 環境変数が https:// で来ても libsql:// に統一
    if env_db_url.startswith("https://"):
        clean_url = env_db_url.replace("https://", "libsql://")
    elif env_db_url.startswith("libsql://"):
        clean_url = env_db_url
    else:
        clean_url = f"libsql://{env_db_url}"
    
    # クエリパラメータを削除（もしあれば）
    SQLALCHEMY_DATABASE_URL = clean_url.split("?")[0]
    
    # 3. connect_args に authToken を追加（これが重要！）
    connect_args = {
        "check_same_thread": False,
        "authToken": auth_token  # ← ここでトークンを渡す
    }
    
    print(f"--- [SETUP] Turso URL: {SQLALCHEMY_DATABASE_URL}")
    print(f"--- [SETUP] Auth token length: {len(auth_token)}")

else:
    # ローカル開発用
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"--- [SETUP] Connecting to Local SQLite: {DB_PATH}")

# --- エンジン作成 ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()