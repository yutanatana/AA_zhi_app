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
    
    # 1. トークンの存在チェック (ここで空なら強制終了させる)
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing or empty in Render Environment Variables !!!")
        sys.exit(1) # アプリを停止
        
    # 2. URLの整形
    # "libsql://" や "https://" を除去し、ホスト名だけにする
    # 例: "libsql://my-db.turso.io" -> "my-db.turso.io"
    clean_host = env_db_url.replace("libsql://", "").replace("https://", "").replace("http://", "").split("?")[0].strip("/")
    
    # 3. 正しい形式でURLを再構築 (ここが最重要)
    # トークンは URL のパラメータ (?authToken=...) として渡す必要があります
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{clean_host}?authToken={auth_token}&secure=true"
    
    print(f"--- [SETUP] Connection URL constructed for: {clean_host}")

else:
    # ローカル開発用
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    # プロジェクト構造に合わせてパス調整が必要な場合はここを変更
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