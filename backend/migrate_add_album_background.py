import sqlite3

# Connect to database
conn = sqlite3.connect('family_memories.db')
cursor = conn.cursor()

try:
    # Add background_image column to albums table
    cursor.execute('ALTER TABLE albums ADD COLUMN background_image TEXT')
    conn.commit()
    print("Successfully added background_image column to albums table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("Column background_image already exists")
    else:
        print(f"Error: {e}")
finally:
    conn.close()
