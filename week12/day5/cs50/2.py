import sqlite3

conn = sqlite3.connect("dese.db")

cursor = conn.cursor()

cursor.execute("SELECT name FROM districts WHERE name LIKE '%(non-op)';")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
