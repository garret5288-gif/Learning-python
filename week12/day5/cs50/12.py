import sqlite3

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()  


cursor.execute(
    """
    SELECT districts.name, per_pupil_expenditure, exemplary FROM districts
    JOIN expenditures ON expenditures.district_id = districts.id
    JOIN staff_evaluations ON staff_evaluations.district_id = districts.id
    WHERE type = "Public School District"
    AND per_pupil_expenditure > (
        SELECT AVG(per_pupil_expenditure)
    FROM expenditures
    )
    AND exemplary > (
        SELECT AVG(exemplary)
    FROM staff_evaluations
    )
    ORDER BY exemplary DESC, per_pupil_expenditure DESC;
    """
)

rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
