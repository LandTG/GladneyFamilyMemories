# Database Backup System

Comprehensive backup system for the TAG Diary database to prevent data loss.

## Features

- ✅ Automatic daily backups
- ✅ Manual backup creation via script or API
- ✅ Rolling backup history (keeps last 30 backups)
- ✅ Safe backup while database is in use
- ✅ Easy restore functionality
- ✅ Admin-only API endpoints

## Quick Start

### 1. Create a Manual Backup

```bash
cd backend
python3 backup_database.py
```

### 2. Setup Automatic Daily Backups (macOS)

```bash
cd backend
./setup_auto_backup.sh
```

This will configure your Mac to automatically backup the database daily at 2:00 AM.

## Manual Backup Commands

### Create a backup
```bash
python3 backup_database.py
```

### List all backups
```bash
python3 backup_database.py list
```

### Restore from a backup
```bash
python3 backup_database.py restore tag_diary_backup_20251202_123019.db
```

## API Endpoints (Admin Only)

### Create a backup via API
```bash
POST /api/admin/backup
Authorization: Bearer <admin_token>
```

### List all backups
```bash
GET /api/admin/backups
Authorization: Bearer <admin_token>
```

### Download a specific backup
```bash
GET /api/admin/backup/{filename}
Authorization: Bearer <admin_token>
```

## Backup Configuration

- **Location**: `backend/backups/`
- **Filename format**: `tag_diary_backup_YYYYMMDD_HHMMSS.db`
- **Retention**: Last 30 backups (automatically removes older backups)
- **Schedule**: Daily at 2:00 AM (configurable in `com.tagdiary.backup.plist`)

## Managing Automatic Backups

### Check if automatic backups are running
```bash
launchctl list | grep tagdiary
```

### Stop automatic backups
```bash
launchctl unload ~/Library/LaunchAgents/com.tagdiary.backup.plist
```

### Start automatic backups
```bash
launchctl load ~/Library/LaunchAgents/com.tagdiary.backup.plist
```

### View backup logs
```bash
tail -f backend/backups/backup.log
```

## Restore Process

1. **List available backups**:
   ```bash
   python3 backup_database.py list
   ```

2. **Choose a backup and restore**:
   ```bash
   python3 backup_database.py restore tag_diary_backup_20251202_120000.db
   ```

   This will:
   - Create a safety backup of your current database
   - Restore the selected backup
   - Restart is required for the backend to pick up changes

3. **Restart the backend** to load the restored database

## Best Practices

1. **Before major changes**: Create a manual backup
   ```bash
   python3 backup_database.py
   ```

2. **Regular testing**: Periodically verify backups are being created
   ```bash
   python3 backup_database.py list
   ```

3. **Off-site backups**: Consider copying backups to cloud storage (Google Drive, Dropbox, etc.)
   ```bash
   # Example: Copy to cloud folder
   cp backups/tag_diary_backup_*.db ~/Google\ Drive/TAG_Diary_Backups/
   ```

4. **Before deployments**: Always backup production database before deploying

## Troubleshooting

### Automatic backups not running

Check the error log:
```bash
cat backend/backups/backup_error.log
```

Verify launchd job is loaded:
```bash
launchctl list | grep tagdiary
```

### Backup fails

Ensure the database file exists:
```bash
ls -lh backend/tag_diary.db
```

Check permissions:
```bash
ls -lh backend/backups/
```

## Production Backups (Railway)

For Railway deployment, backups work via the API endpoints. You can:

1. Set up a cron job to hit the backup endpoint daily
2. Use Railway's built-in database backup features
3. Manually trigger backups from your admin interface

## File Structure

```
backend/
├── backup_database.py          # Main backup script
├── setup_auto_backup.sh        # Setup automatic backups
├── com.tagdiary.backup.plist  # launchd configuration
├── backups/                    # Backup storage
│   ├── tag_diary_backup_*.db  # Backup files
│   ├── backup.log             # Backup logs
│   └── backup_error.log       # Error logs
└── tag_diary.db               # Main database
```

## Support

If you encounter issues with the backup system, check:
1. Backup logs: `backend/backups/backup.log`
2. Error logs: `backend/backups/backup_error.log`
3. Database exists: `ls -lh backend/tag_diary.db`
