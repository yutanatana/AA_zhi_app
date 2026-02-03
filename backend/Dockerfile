# 軽量なPythonイメージを使用
FROM python-3.12.8

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 先にライブラリ定義だけコピー（キャッシュ効率のため）
COPY requirements.txt .

# ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# FastAPI起動 (Docker内では host=0.0.0.0 が必須)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]