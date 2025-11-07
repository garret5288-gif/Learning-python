import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()

cursor.execute(
    """
    SELECT name, pupils FROM districts
    JOIN expenditures ON expenditures.district_id = districts.id;
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()