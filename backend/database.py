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
print(f"--- [DEBUG] Auth token first 20 chars: {auth_token[:20] if auth_token else 'N/A'}...")

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    print(f"--- [SETUP] Detected Turso Database ---")
    
    # 1. トークンの存在チェック
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing !!!")
        sys.exit(1)
    
    # 2. URL の正規化 - libsql:// を https:// に変換
    if env_db_url.startswith("libsql://"):
        host = env_db_url.replace("libsql://", "")
    elif env_db_url.startswith("https://"):
        host = env_db_url.replace("https://", "")
    else:
        host = env_db_url
    
    # クエリパラメータを削除
    host = host.split("?")[0]
    
    # 3. sqlite+libsql:// プロトコルで https:// を使う
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://https://{host}?authToken={auth_token}"
    
    print(f"--- [SETUP] Connecting to: sqlite+libsql://https://{host}?authToken=***")

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
        echo=False,
        pool_pre_ping=True
    )
    
    # 接続テスト
    print("--- [SETUP] Testing connection...")
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print(f"--- [SETUP] Connection test successful! Result: {result.fetchone()}")
    
    print("--- [SETUP] Engine created successfully!")
    
except Exception as e:
    print(f"!!! ERROR: {type(e).__name__}: {e}")
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