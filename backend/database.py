import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import URL # <--- これを追加

# --- 環境変数の取得 ---
env_db_url = os.getenv("DATABASE_URL", "").strip()
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    print(f"--- [SETUP] Detected Turso Database ---")
    
    # 1. トークンの存在チェック
    if not auth_token:
        print("!!! CRITICAL ERROR: DATABASE_AUTH_TOKEN is missing provided !!!")
        sys.exit(1)
        
    # 2. ホスト名の抽出
    # "libsql://" や "https://" を取り除き、クエリパラメータも削除してホスト名だけにする
    # 例: "libsql://my-db.turso.io" -> "my-db.turso.io"
    clean_host = env_db_url.replace("libsql://", "").replace("https://", "").replace("http://", "").split("?")[0].strip("/")
    
    # 3. URLオブジェクトを使って安全に構築 (ここが修正の肝)
    # これにより、トークン内の記号が自動的に正しく変換(エンコード)されます
    db_url_obj = URL.create(
        drivername="sqlite+libsql",
        host=clean_host,
        query={
            "authToken": auth_token,
            "secure": "true"
        }
    )
    
    # URLオブジェクトを文字列ではなく、そのままエンジンに渡すか、render_as_stringで確認
    SQLALCHEMY_DATABASE_URL = db_url_obj
    
    print(f"--- [SETUP] Connection URL constructed for host: {clean_host}")

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