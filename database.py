import sqlite3

connection = sqlite3.connect(
    "protasker.db",
    check_same_thread=False
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    priority TEXT
)
""")

connection.commit()