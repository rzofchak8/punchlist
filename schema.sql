-- Users
CREATE TABLE user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL
);

-- Houses
CREATE TABLE house (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    address     TEXT,
    is_complete BOOLEAN DEFAULT 0,
    note        TEXT
);

-- Rooms
CREATE TABLE room (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    house_id    INTEGER NOT NULL,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT,
    FOREIGN KEY (house_id) REFERENCES house(id) ON DELETE CASCADE
);

-- Photos
CREATE TABLE photo (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id     INTEGER NOT NULL,
    path        TEXT    NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
);

-- Categories
CREATE TABLE category (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    symbolMeta TEXT
);

-- Category-House mapping
CREATE TABLE categoryHouse (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    house_id    INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    passkey     TEXT,
    FOREIGN KEY (house_id)    REFERENCES house(id)    ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- Task Types (optional)
CREATE TABLE taskType (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT    NOT NULL
);

-- Task Lists
CREATE TABLE taskList (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id  INTEGER NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE
);

-- Tasks
CREATE TABLE task (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id     INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    status      TEXT    DEFAULT 'pending',
    priority    INTEGER DEFAULT 0,
    type_id     INTEGER,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id)     REFERENCES room(id)     ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (type_id)     REFERENCES taskType(id)
);

-- Logs
CREATE TABLE log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    contents  TEXT    NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migrations
CREATE TABLE migration (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    contents  TEXT    NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
