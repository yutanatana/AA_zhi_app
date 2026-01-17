import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- ローカルパス設定 ---
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BACKEND_DIR), "sql_app.db")

# --- 環境変数の取得 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- デバッグログ (RenderのLogsで確認してください) ---
print(f"-------- [DEBUG START] --------")
print(f"DATABASE_URL (Raw): {env_db_url}")
# トークンはセキュリティのため先頭10文字だけ表示し、残りは隠す
masked_token = (auth_token[:10] + "...") if auth_token else "EMPTY/NONE"
print(f"DATABASE_AUTH_TOKEN: {masked_token}")
print(f"-------- [DEBUG END] --------")

# --- 接続先URLの決定 ---
if "turso.io" in env_db_url:
    # URLから不要なプロトコルと、万が一含まれているクエリパラメータ(?以降)を削除
    clean_host = env_db_url.split("://")[-1].split("?")[0].strip("/")
    
    # URLを再構築
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{clean_host}?authToken={auth_token}&secure=true"
    print(f"-------- [DEBUG] Final URL: sqlite+libsql://{clean_host}?authToken=***&secure=true --------")

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