#sqlite table creation
CREATE TABLE channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server TEXT NOT NULL,
    channel TEXT NOT NULL
);