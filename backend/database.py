import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlencode

# --- 環境変数の取得 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- デバッグ出力 ---
print(f"--- [DEBUG] DATABASE_URL: {env_db_url}")
print(f"--- [DEBUG] Auth token exists: {bool(auth_token)}")

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    print(f"--- [SETUP] Detected Turso Database ---")
    
    # 1. トークンの存在チェック
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing !!!")
        sys.exit(1)
    
    # 2. libsql:// を sqlite+libsql:// に変換
    base_url = env_db_url.replace("libsql://", "sqlite+libsql://")
    
    # クエリパラメータを削除（もし既に含まれていたら）
    base_url = base_url.split("?")[0]
    
    # 3. authToken をクエリパラメータとして追加
    params = {
        "authToken": auth_token,
        "secure": "true"
    }
    query_string = urlencode(params)
    SQLALCHEMY_DATABASE_URL = f"{base_url}?{query_string}"
    
    print(f"--- [SETUP] Final URL: {base_url}?authToken=***&secure=true")

else:
    # ローカル開発用
    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"--- [SETUP] Connecting to Local SQLite: {DB_PATH}")

# --- エンジン作成 ---
print(f"--- [SETUP] Creating engine...")

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