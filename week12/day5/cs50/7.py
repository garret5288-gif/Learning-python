import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()

cursor.execute(
    """
    SELECT schools.name FROM districts
    JOIN schools ON schools.district_id = districts.id
    WHERE districts.name = "Cambridge";
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()