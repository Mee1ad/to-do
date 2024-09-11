#!/bin/bash

TIMESTAMP=$(date +%F_%T)
BACKUP_FILE="/backup/db_backup_${TIMESTAMP}.sql"

pg_dump -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Backup successful: $BACKUP_FILE"
else
  echo "Backup failed"
  rm -f "$BACKUP_FILE"
  exit 1
fi
