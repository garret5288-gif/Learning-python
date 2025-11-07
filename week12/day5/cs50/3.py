import sqlite3

conn = sqlite3.connect("dese.db")

cursor = conn.cursor()

cursor.execute("SELECT AVG(per_pupil_expenditure) AS 'Average District Per-Pupil Expenditure' FROM expenditures;")
row = cursor.fetchone()
# Use cursor.description to show the column name
col_name = cursor.description[0][0]
value = row[0]
print(f"{col_name}: {value if value is not None else 'N/A'}")
conn.close()