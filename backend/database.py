import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 環境変数の読み込み ---
# Renderで設定されている "libsql://..." 形式のURL
env_db_url = os.getenv("DATABASE_URL", "").strip()
# Renderで設定されているトークン
auth_token = os.getenv("DATABASE_AUTH_TOKEN", "").strip()

# --- デバッグ出力（ログで変数が空かを確認するため） ---
print(f"--- DEBUG: URL Length: {len(env_db_url)}")
print(f"--- DEBUG: Token Length: {len(auth_token)}") # ここが 0 なら環境変数が読めていません

# --- 接続設定 ---
connect_args = {"check_same_thread": False}

if "turso.io" in env_db_url:
    # URLのプロトコル部分を修正 (libsql:// -> sqlite+libsql://)
    # urlは "sqlite+libsql://db-name.turso.io" のようなシンプルな形にします
    url = env_db_url.replace("libsql://", "sqlite+libsql://").replace("https://", "sqlite+libsql://")
    
    # 重要: トークンは URL に含めず、connect_args で渡す
    connect_args["authToken"] = auth_token
    connect_args["secure"] = True
    
    SQLALCHEMY_DATABASE_URL = url
    print(f"--- DEBUG: Connecting to Turso (Token passed via args) ---")
else:
    # ローカル用
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"--- DEBUG: Connecting to Local SQLite ---")

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