#!/bin/bash
# Setup automatic daily database backups using launchd (macOS)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="com.tagdiary.backup.plist"
PLIST_SOURCE="$SCRIPT_DIR/$PLIST_FILE"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_FILE"

echo "🔧 Setting up automatic database backups..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Copy plist file to LaunchAgents
echo "📋 Installing launchd configuration..."
cp "$PLIST_SOURCE" "$PLIST_DEST"

# Load the launchd job
echo "⚡ Loading backup schedule..."
launchctl unload "$PLIST_DEST" 2>/dev/null  # Unload if already loaded
launchctl load "$PLIST_DEST"

echo ""
echo "✅ Automatic backups are now configured!"
echo ""
echo "📅 Schedule: Daily at 2:00 AM"
echo "📁 Backup location: $SCRIPT_DIR/backups/"
echo "📝 Logs: $SCRIPT_DIR/backups/backup.log"
echo ""
echo "Commands:"
echo "  - Manual backup:    python3 backup_database.py"
echo "  - List backups:     python3 backup_database.py list"
echo "  - Restore backup:   python3 backup_database.py restore <filename>"
echo ""
echo "  - Stop auto backup: launchctl unload $PLIST_DEST"
echo "  - Start auto backup: launchctl load $PLIST_DEST"
echo ""
