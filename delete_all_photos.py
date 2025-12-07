#!/usr/bin/env python3
import sqlite3
import os
from pathlib import Path

# Database path
db_path = "/Users/tomgladney1/GladneyFamilyMemories/backend/tag_diary.db"
backend_path = Path("/Users/tomgladney1/GladneyFamilyMemories/backend")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all photos
cursor.execute("SELECT id, filename, file_path FROM photos")
photos = cursor.fetchall()

print(f"Found {len(photos)} photos to delete")

deleted_count = 0
file_deleted_count = 0
for photo_id, filename, file_path in photos:
    print(f"\nDeleting photo ID {photo_id}: {filename}")

    # Delete physical file
    full_path = backend_path / file_path
    try:
        if full_path.exists():
            full_path.unlink()
            file_deleted_count += 1
            print(f"  ✓ Deleted file: {file_path}")
        else:
            print(f"  ! File not found: {file_path}")
    except Exception as e:
        print(f"  ✗ Error deleting file: {e}")

    # Delete from database
    try:
        # First delete from album_photos (if any)
        cursor.execute("DELETE FROM album_photos WHERE photo_id = ?", (photo_id,))

        # Delete from vignette_photos (if any)
        cursor.execute("DELETE FROM vignette_photos WHERE photo_id = ?", (photo_id,))

        # Delete from photo_people (if any)
        cursor.execute("DELETE FROM photo_people WHERE photo_id = ?", (photo_id,))

        # Finally delete the photo
        cursor.execute("DELETE FROM photos WHERE id = ?", (photo_id,))

        deleted_count += 1
        print(f"  ✓ Deleted from database")
    except Exception as e:
        print(f"  ✗ Error deleting from database: {e}")
        conn.rollback()
        continue

# Commit all deletions
conn.commit()
conn.close()

print(f"\n{'='*50}")
print(f"Successfully deleted {deleted_count} photos from database")
print(f"Successfully deleted {file_deleted_count} physical files")
print(f"{'='*50}")
