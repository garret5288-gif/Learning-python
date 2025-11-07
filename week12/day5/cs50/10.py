import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()


cursor.execute(
    """
    SELECT name, per_pupil_expenditure  FROM districts
    JOIN expenditures ON expenditures.district_id = districts.id
    WHERE type = "Public School District"
    ORDER BY per_pupil_expenditure DESC
    LIMIT 10;
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()

