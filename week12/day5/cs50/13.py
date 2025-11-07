import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()


cursor.execute(
    """
    SELECT name, dropped FROM schools
    JOIN graduation_rates ON graduation_rates.school_id = schools.id
    WHERE type = "Public School"
    ORDER BY dropped DESC, name;
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
