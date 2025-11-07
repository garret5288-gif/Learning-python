import sqlite3

conn = sqlite3.connect("dese.db")

cursor = conn.cursor()
cursor.execute("SELECT name, city FROM schools WHERE type = 'Public School';")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
