import csv
import pymysql


# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='G8nFtDr6@_@'
)

cursor = connection.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS basketball_players")
cursor.execute("USE basketball_players")

# Create a table to store the player data
cursor.execute("""
CREATE TABLE IF NOT EXISTS basic_info (
    Player VARCHAR(100),
    Pos VARCHAR(10),
    Ht VARCHAR(10),
    Wt VARCHAR(10)
)
""")

# Create a new table for the player stats
cursor.execute("""
CREATE TABLE IF NOT EXISTS career_summary (
    Player VARCHAR(100),
    G INT,
    PTS FLOAT,
    TRB FLOAT,
    AST FLOAT
)
""")

# Open the CSV file (basic_info.csv)
with open('D:\\write_code_every_day\\NBA-reference\\output\\basic_info.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row

    for row in reader:
        # Insert data into the basic_info table
        cursor.execute("""
        INSERT INTO basic_info (Player, Pos, Ht, Wt)
        VALUES (%s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3]))

# Open the CSV file (career_summary.csv)
with open('D:\\write_code_every_day\\NBA-reference\\output\\career_summary.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    
    for row in reader:
        # Insert data into the career_summary table
        cursor.execute("""
        INSERT INTO career_summary (Player, G, PTS, TRB, AST)
        VALUES (%s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3] if row[3] != '-' else None, row[4]))

# Commit the changes
connection.commit()

# display all data in db
cursor.execute("SELECT * FROM basic_info")
rows = cursor.fetchall()

for row in rows:
    print(str(row).encode('utf-8'))

cursor.execute("SELECT * FROM career_summary")
rows = cursor.fetchall()

for row in rows:
    print(str(row).encode('utf-8'))

# Close the connection
cursor.close()
connection.close()
