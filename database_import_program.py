import sqlite3
import csv

conn = sqlite3.connect('baseball_history.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Events (
    Year INTEGER,
    Event TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Stats (
    Year INTEGER,
    Statistic TEXT
)
""")

try:
    with open('mlb_years.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 
        for row in reader:
            year, event, stat = row
            try:
                year = int(year)
            except ValueError:
                continue
            event = event.strip()
            stat = stat.strip()
            cursor.execute("SELECT 1 FROM Events WHERE Year = ? AND Event = ?", (year, event))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Events (Year, Event) VALUES (?, ?)", (year, event))
            cursor.execute("SELECT 1 FROM Stats WHERE Year = ? AND Statistic = ?", (year, stat))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Stats (Year, Statistic) VALUES (?, ?)", (year, stat))

    conn.commit()
    print("Data imported into two tables: Events and Stats")
except Exception as e:
    conn.rollback()
    print("Error:", e)

conn.close()