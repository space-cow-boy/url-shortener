import sqlite3

# connect to (or create) database
conn = sqlite3.connect("urls.db")

# create cursor
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL
)
""")

# save changes
conn.commit()

# close connection
conn.close()

print("Table created successfully")
