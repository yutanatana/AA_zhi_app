import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 環境変数の取得 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- デバッグ出力 ---
print(f"--- [DEBUG] DATABASE_URL: {env_db_url}")
print(f"--- [DEBUG] Auth token exists: {bool(auth_token)}")
print(f"--- [DEBUG] Auth token length: {len(auth_token) if auth_token else 0}")

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    print(f"--- [SETUP] Detected Turso Database ---")
    
    # 1. トークンの存在チェック
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing !!!")
        sys.exit(1)
    
    # 2. libsql:// を sqlite+libsql:// に変換
    # sqlalchemy-libsql は sqlite+libsql:// をドライバー名として使用
    SQLALCHEMY_DATABASE_URL = env_db_url.replace("libsql://", "sqlite+libsql://")
    
    # 3. connect_args に authToken を追加
    connect_args = {
        "check_same_thread": False,
        "authToken": auth_token
    }
    
    print(f"--- [SETUP] Final URL: {SQLALCHEMY_DATABASE_URL}")

else:
    # ローカル開発用
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"--- [SETUP] Connecting to Local SQLite: {DB_PATH}")

# --- エンジン作成 ---
print(f"--- [SETUP] Creating engine with connect_args: {list(connect_args.keys())}")

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args=connect_args,
        echo=False
    )
    print("--- [SETUP] Engine created successfully!")
except Exception as e:
    print(f"!!! ERROR creating engine: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()