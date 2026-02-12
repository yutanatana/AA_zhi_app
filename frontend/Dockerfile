# Node.jsのイメージ
FROM node:20-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係のインストール
COPY package.json package-lock.json* ./
RUN npm install

# ソースコードをコピー
COPY . .

# 開発サーバー起動 (Docker内では --host が必須)
CMD ["npm", "run", "dev", "--", "--host"]