-- SQLite
CREATE TABLE inventory (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, units INTEGER NOT NULL, lower_limit INTEGER);

ALTER TABLE inventory ADD COLUMN user_id INTEGER;

ALTER TABLE inventory ADD COLUMN time;

UPDATE inventory SET time = NOT NULL;

ALTER TABLE inventory RENAME TO _table1_old;

CREATE TABLE inventory
( id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  units INTEGER NOT NULL,
  lower_limit INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  time DATETIME DEFAULT CURRENT_TIMESTAMP 
);

INSERT INTO inventory(id,name, units, lower_limit, user_id, time)
  SELECT id, name, units, lower_limit, user_id, time 
  FROM _table1_old;

DROP TABLE 