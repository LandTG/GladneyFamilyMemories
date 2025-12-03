import sqlite3
from pathlib import Path

db_path = Path("tag_diary.db")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Add sort_order to photos table
    cursor.execute("PRAGMA table_info(photos)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'sort_order' not in columns:
        print("Adding sort_order column to photos table...")
        cursor.execute("ALTER TABLE photos ADD COLUMN sort_order INTEGER DEFAULT 0")

        # Set sort_order based on created_at for existing photos
        cursor.execute("""
            UPDATE photos
            SET sort_order = (
                SELECT COUNT(*)
                FROM photos p2
                WHERE p2.created_at <= photos.created_at
            )
        """)

        print("✓ Successfully added sort_order column to photos table")
    else:
        print("sort_order column already exists in photos table")

    # Add sort_order to albums table
    cursor.execute("PRAGMA table_info(albums)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'sort_order' not in columns:
        print("Adding sort_order column to albums table...")
        cursor.execute("ALTER TABLE albums ADD COLUMN sort_order INTEGER DEFAULT 0")

        # Set sort_order based on created_at for existing albums
        cursor.execute("""
            UPDATE albums
            SET sort_order = (
                SELECT COUNT(*)
                FROM albums a2
                WHERE a2.created_at <= albums.created_at
            )
        """)

        print("✓ Successfully added sort_order column to albums table")
    else:
        print("sort_order column already exists in albums table")

    conn.commit()
    conn.close()
    print("\n✓ Migration completed successfully!")
else:
    print(f"Database not found at {db_path}")
