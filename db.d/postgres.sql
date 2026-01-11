-- 本番デプロイようのPostgreSQL用スキーマ定義
-- 1. グループテーブル
CREATE TABLE groups (
    id UUID PRIMARY KEY, -- PostgresはUUID型が使える
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. メンバーテーブル
CREATE TABLE members (
    id SERIAL PRIMARY KEY, -- 自動採番
    group_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    archived BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

-- 3. 支出テーブル
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    group_id UUID NOT NULL,
    paid_by_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (paid_by_id) REFERENCES members(id) ON DELETE CASCADE
);

-- 4. 割り勘内訳テーブル
CREATE TABLE expense_splits (
    id SERIAL PRIMARY KEY,
    expense_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);