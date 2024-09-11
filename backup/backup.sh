#!/bin/bash

# Set the timestamp and backup file path
TIMESTAMP=$(date +%F_%T)
BACKUP_FILE="/backup/db_backup_${TIMESTAMP}.sql"

# Set the password environment variable
export PGPASSWORD="$POSTGRES_PASSWORD"

# Run the pg_dump command to backup the database, specifying the host
pg_dump -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c > "$BACKUP_FILE"

# Check if the backup was successful
if [ $? -eq 0 ]; then
  echo "Backup successful: $BACKUP_FILE"
else
  echo "Backup failed"
  # Optionally, remove the failed backup file
  rm -f "$BACKUP_FILE"
  exit 1
fi

# Number of backups to keep
NUM_BACKUPS=30

# Remove old backups, keeping only the most recent $NUM_BACKUPS files
cd /backup
ls -t | grep '^db_backup_' | sed -e "1,${NUM_BACKUPS}d" | xargs -d '\n' rm -f
