import sqlite3  

conn = sqlite3.connect("dese.db")
cursor = conn.cursor()


cursor.execute(
    """
    SELECT city, COUNT(name) FROM schools
    WHERE type = "Public School"
    GROUP BY city
    HAVING COUNT(name) <= 3
    ORDER BY COUNT(name) DESC, city;
    """
)
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()