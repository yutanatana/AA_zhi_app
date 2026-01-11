-- 外部キー制約を有効化（SQLite特有）
PRAGMA foreign_keys = ON;

-- 1. グループテーブル
CREATE TABLE groups (
    id TEXT PRIMARY KEY, -- UUIDを文字列として格納
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. メンバーテーブル
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id TEXT NOT NULL,
    name TEXT NOT NULL,
    archived INTEGER DEFAULT 0, -- 0: false, 1: true
    CONSTRAINT fk_group
        FOREIGN KEY (group_id) 
        REFERENCES groups (id)
        ON DELETE CASCADE -- グループが消えたらメンバーも消える
);

-- 3. 支出テーブル（レシート情報）
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id TEXT NOT NULL,
    paid_by_id INTEGER NOT NULL, -- 立替えた人
    amount INTEGER NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_group_expense
        FOREIGN KEY (group_id) 
        REFERENCES groups (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_payer
        FOREIGN KEY (paid_by_id) 
        REFERENCES members (id)
        ON DELETE CASCADE
);

-- 4. 割り勘内訳テーブル（誰が負担するか）
CREATE TABLE expense_splits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL, -- 負担する人
    CONSTRAINT fk_expense
        FOREIGN KEY (expense_id) 
        REFERENCES expenses (id)
        ON DELETE CASCADE, -- 支出自体が消えたら内訳も消える
    CONSTRAINT fk_member_split
        FOREIGN KEY (member_id) 
        REFERENCES members (id)
        ON DELETE CASCADE
);