import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- ローカルパス設定 ---
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")

# --- 接続先URLの決定 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# Turso (turso.io) を使用するかどうかの判定
if "turso.io" in env_db_url:
    # 1. プロトコル（libsql:// や https://）と末尾のスラッシュを強制的に削除
    #    例: "libsql://my-db.turso.io/" -> "my-db.turso.io"
    clean_host = env_db_url.replace("libsql://", "").replace("https://", "").replace("http://", "").strip("/")
    
    # 2. 正しい形式 (sqlite+libsql://ドメイン) で再構築
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{clean_host}?auth_token={auth_token}&secure=true"
    
    # デバッグ用ログ（RenderのLogsで確認できます）
    print(f"-------- [DEBUG] Connecting to Turso Host: {clean_host} --------")

else:
    # ローカル開発用
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print("-------- [DEBUG] Connecting to Local SQLite --------")

# --- エンジン作成 ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()