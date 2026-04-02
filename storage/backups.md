# Web Server Backup Documentation

---

## 1. Script Content

Below is the bash script (`backup_web.sh`) used to archive the Nginx web server configuration, move it to the RAID array, and enforce a 7-day retention policy.

```bash id="f82k1a"
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
```

---

## 2. Cron Logic

To automate the backup, I added the following entry to the root crontab using:

```bash id="g91lqp"
sudo crontab -e
```

### Cron Entry

```bash id="x92pld"
0 2 * * * /home/ubuntu/backup_web.sh
```

### Explanation of the Cron Expression (`0 2 * * *`)

* **0 (Minute):** Runs at minute 0 (top of the hour)
* **2 (Hour):** Runs at 2:00 AM (server time)
* *** (Day of Month):** Every day
* *** (Month):** Every month
* *** (Day of Week):** Every day of the week

**Overall:** The script runs automatically **once per day at 2:00 AM**.

---

## 3. Verification

Below is where you should include a screenshot showing multiple backup archives stored on the RAID array:

```bash id="0g7m3b"
ls -l /mnt/raid_data/backups
```

*(Insert your screenshot here)*

---

## 4. Log Check

Below is the syslog output proving that the cron daemon successfully executed the backup script:

```text id="m3c9sp"
Apr  2 13:01:01 ip-10-0-20-196 CRON[81234]: (ubuntu) CMD (/home/ubuntu/backup_web.sh)
```

---

**End of Document**
