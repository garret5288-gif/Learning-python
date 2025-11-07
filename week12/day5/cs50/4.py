import sqlite3
import os

def main():
    # Use path relative to this script so it works from any cwd
    db_path = os.path.join(os.path.dirname(__file__), "dese.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # All cities with their public school counts (descending)
    cursor.execute(
        """
        SELECT city, COUNT(name) AS public_school_count
        FROM schools
        WHERE type = 'Public School'
        GROUP BY city
        ORDER BY public_school_count DESC, city
        """
    )
    rows = cursor.fetchall()
    print("All cities (city\tpublic_school_count):")
    for city, count in rows:
        print(f"{city}\t{count}")

    # Top 10 cities by public school count
    cursor.execute(
        """
        SELECT city, COUNT(name) AS public_school_count
        FROM schools
        WHERE type = 'Public School'
        GROUP BY city
        ORDER BY public_school_count DESC, city
        LIMIT 10
        """
    )
    top_rows = cursor.fetchall()
    print("\nTop 10 cities by public school count:")
    for city, count in top_rows:
        print(f"{city}\t{count}")

    conn.close()

if __name__ == "__main__":
    main()
