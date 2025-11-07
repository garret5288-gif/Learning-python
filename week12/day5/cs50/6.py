import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()

cursor.execute(
    """
    SELECT name FROM schools
    JOIN graduation_rates ON graduation_rates.school_id = schools.id
    WHERE graduated = 100;
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()