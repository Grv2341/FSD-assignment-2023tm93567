import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute a query to select all records from the users table
cursor.execute("SELECT * FROM users")

# Fetch all rows from the result
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

cursor.execute("SELECT * FROM sessions")

# Fetch all rows from the result
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()