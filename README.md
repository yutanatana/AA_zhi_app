 バックエンドは FastAPI + SQLite、フロントエンドは Vue.js (Composition API) + Axios で実装しています。
  URL共有機能は、UUID v4 を使用して推測困難なIDを発行することで実現しています。

  1. 起動方法

  ターミナルを2つ開き、それぞれで以下のコマンドを実行してください。

  バックエンド (Port: 8000)
   1 cd backend
   2 pip install -r requirements.txt
   3 uvicorn main:app --reload

  フロントエンド (Port: 5173)

   1 cd frontend
   2 npm run dev

  起動後、ブラウザで http://localhost:5173 にアクセスしてください。

  ---

  2. 実装ファイルの内容

  backend/main.py
  APIエンドポイントとデータベース設定です。
   - POST /bills: 割り勘データの作成（UUID発行）
   - GET /bills/{bill_id}: データの取得
   - CORS設定: フロントエンド（5173番ポート等）からのアクセスを許可

  frontend/src/components/SplitBill.vue
  この1つのコンポーネントで以下の機能を兼ねています。
   - 作成モード: URLがない場合（ルートパス /）。金額と名目を入力して保存。
   - 表示モード: URLにIDがある場合（/:id）。保存された割り勘情報を表示し、URLコピー機能を提供。

  3. ディレクトリ構成の確認

    1 /Users/y-tanaka/project/割り勘アプリ/AA_zhi_app/
    2 ├── backend/
    3 │   ├── main.py
    4 │   └── requirements.txt
    5 └── frontend/
    6     ├── package.json
    7     ├── vite.config.js
    8     └── src/
    9         ├── App.vue
   10         ├── main.js
   11         ├── components/
   12         │   └── SplitBill.vue
   13         └── router/
   14             └── index.js

  これでMVP（最小機能版）としての動作確認が可能です。