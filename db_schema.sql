--DROP TABLE IF EXISTS users;
--DROP TABLE IF EXISTS submissions;
--DROP TABLE IF EXISTS master_record;

CREATE TABLE IF NOT EXISTS users (
    user TEXT PRIMARY KEY,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    datetime_id INTEGER NOT NULL,

    accuracy REAL NOT NULL,
    f1 REAL NOT NULL,
    auc REAL NOT NULL,
    ap REAL NOT NULL,

    note TEXT,
    prediction TEXT,

    FOREIGN KEY (user) REFERENCES users(user),
    UNIQUE (user, datetime_id)
);


CREATE TABLE IF NOT EXISTS master_record (
    y_true TEXT,

    final_date TEXT
);
INSERT INTO master_record(y_true, final_date)
SELECT '[]',''
WHERE NOT EXISTS (SELECT * FROM master_record)