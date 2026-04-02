# Web Server Backup Documentation

## 1. Script Content
Below is the bash script (`backup_web.sh`) used to archive the Nginx configuration, move it to the RAID array, and enforce a 7-day retention policy.

\`\`\`bash
#!/bin/bash

# --- Variables ---
SOURCE_DIR="/etc/nginx"
BACKUP_DIR="/mnt/raid_data/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
ARCHIVE_NAME="web-config-$TIMESTAMP.tar.gz"

# 1. Ensure the backup directory exists on the RAID
mkdir -p "$BACKUP_DIR"

# 2. Create the compressed archive (tar.gz) and send it directly to the RAID
tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" "$SOURCE_DIR"

# 3. Retention Policy (Extra Credit): Find and delete backups older than 7 days
find "$BACKUP_DIR" -type f -name "web-config-*.tar.gz" -mtime +7 -delete

echo "Backup completed successfully on $TIMESTAMP"
\`\`\`

## 2. Cron Logic
To automate the backup, I added the following entry to the root crontab (`sudo crontab -e`):

\`\`\`bash
0 2 * * * /home/ubuntu/backup_web.sh
\`\`\`

**Explanation of the Cron Expression (`0 2 * * *`):**
* **`0` (Minute):** Runs exactly at the top of the hour (the 0th minute).
* **`2` (Hour):** Runs at 2:00 AM (server time).
* **`*` (Day of Month):** Runs every day of the month.
* **`*` (Month):** Runs every month of the year.
* **`*` (Day of Week):** Runs every day of the week.
* **Overall:** This script triggers once daily at exactly 2:00 AM.

## 3. Verification
*Below is a screenshot showing multiple backup archives successfully stored on the RAID array:*

![RAID Backups Screenshot](link-to-your-screenshot-image.png)

## 4. Log Check
*Below is the syslog output proving that the system's cron daemon successfully triggered the backup script:*

\`\`\`text
[Paste your cron log output right here!]
\`\`\`
