import sqlite3

conn = sqlite3.connect("baseball_history.db")
cursor = conn.cursor()

year = 1901
cursor.execute("""
SELECT e.Year, e.Event, s.Statistic
FROM Events e
JOIN Stats s ON e.Year = s.Year
WHERE e.Year = ?
""", (year,))

rows = cursor.fetchall()
print(f"Results for year {year}:")
for row in rows:
    print(row)

event_name = "Home Runs"
cursor.execute("""
SELECT e.Year, e.Event, s.Statistic
FROM Events e
JOIN Stats s ON e.Year = s.Year
WHERE e.Event = ?
""", (event_name,))

rows = cursor.fetchall()
print(f"\nResults for event '{event_name}':")
for row in rows:
    print(row)

conn.close()