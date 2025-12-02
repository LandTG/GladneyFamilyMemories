#!/usr/bin/env python3
"""
Automated database backup script for tag_diary.db
Creates timestamped backups and maintains a rolling history.
"""

import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


# Configuration
DB_PATH = Path(__file__).parent / "tag_diary.db"
BACKUP_DIR = Path(__file__).parent / "backups"
MAX_BACKUPS = 30  # Keep last 30 backups (1 month if daily)


def create_backup():
    """Create a timestamped backup of the database"""

    # Ensure backup directory exists
    BACKUP_DIR.mkdir(exist_ok=True)

    # Check if database exists
    if not DB_PATH.exists():
        print(f"⚠️  Database not found at {DB_PATH}")
        return False

    # Create timestamp for backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"tag_diary_backup_{timestamp}.db"
    backup_path = BACKUP_DIR / backup_filename

    try:
        # Use SQLite backup API for safe backup (even if database is in use)
        print(f"📦 Creating backup: {backup_filename}")

        # Connect to source database
        source_conn = sqlite3.connect(str(DB_PATH))

        # Connect to backup database
        backup_conn = sqlite3.connect(str(backup_path))

        # Perform the backup
        with backup_conn:
            source_conn.backup(backup_conn)

        source_conn.close()
        backup_conn.close()

        # Get backup file size
        backup_size = backup_path.stat().st_size
        backup_size_kb = backup_size / 1024

        print(f"✅ Backup created successfully!")
        print(f"   Location: {backup_path}")
        print(f"   Size: {backup_size_kb:.2f} KB")

        # Clean up old backups
        cleanup_old_backups()

        return True

    except Exception as e:
        print(f"❌ Backup failed: {e}")
        # Remove incomplete backup file if it exists
        if backup_path.exists():
            backup_path.unlink()
        return False


def cleanup_old_backups():
    """Remove old backups, keeping only the most recent MAX_BACKUPS"""

    # Get all backup files
    backup_files = sorted(
        BACKUP_DIR.glob("tag_diary_backup_*.db"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    # Remove old backups if we have more than MAX_BACKUPS
    if len(backup_files) > MAX_BACKUPS:
        files_to_remove = backup_files[MAX_BACKUPS:]
        print(f"\n🗑️  Removing {len(files_to_remove)} old backup(s)...")

        for old_backup in files_to_remove:
            try:
                old_backup.unlink()
                print(f"   Removed: {old_backup.name}")
            except Exception as e:
                print(f"   Failed to remove {old_backup.name}: {e}")

    print(f"\n📊 Total backups: {min(len(backup_files), MAX_BACKUPS)}")


def list_backups():
    """List all available backups"""

    backup_files = sorted(
        BACKUP_DIR.glob("tag_diary_backup_*.db"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not backup_files:
        print("No backups found.")
        return

    print(f"\n📋 Available backups ({len(backup_files)}):\n")

    for i, backup_file in enumerate(backup_files, 1):
        size_kb = backup_file.stat().st_size / 1024
        modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
        print(f"{i:2d}. {backup_file.name}")
        print(f"    Size: {size_kb:.2f} KB | Created: {modified.strftime('%Y-%m-%d %H:%M:%S')}")


def restore_backup(backup_filename):
    """Restore database from a specific backup file"""

    backup_path = BACKUP_DIR / backup_filename

    if not backup_path.exists():
        print(f"❌ Backup file not found: {backup_filename}")
        return False

    # Create a backup of current database before restoring
    if DB_PATH.exists():
        print("📦 Creating safety backup of current database...")
        safety_backup = DB_PATH.parent / f"tag_diary_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, safety_backup)
        print(f"   Safety backup: {safety_backup.name}")

    try:
        print(f"\n🔄 Restoring from: {backup_filename}")
        shutil.copy2(backup_path, DB_PATH)
        print(f"✅ Database restored successfully!")
        return True

    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            list_backups()
        elif command == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Usage:")
            print("  python3 backup_database.py          # Create backup")
            print("  python3 backup_database.py list     # List all backups")
            print("  python3 backup_database.py restore <filename>  # Restore from backup")
    else:
        # Default: create backup
        create_backup()
