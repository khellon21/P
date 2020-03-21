# Permissions Configuration & SSH Jail Setup

## User Access Matrix

| User           | Primary Group | Edit Access | Read Access |
| :------------- | :------------ | :---------- | :---------- |
| `owner`        | `webadmins`   | Main & Menu | Full        |
| `tech-support` | `webadmins`   | Main & Menu | Full        |
| `staff-member` | `menustaff`   | Menu Only   | Menu Only   |

---

## Command Logic

### `useradd -m` vs `useradd -M`

The `-m` flag creates a standard home directory for a user (e.g., `/home/username`), whereas the `-M` flag explicitly tells the system *not* to create a home directory. We chose `-M` for this scenario because these are "virtual" users whose sole purpose is to manage web content inside the `/var/www/` directories. Creating home directories for them would unnecessarily clutter the system and increase the attack surface.

### The `/usr/sbin/nologin` Shell

Setting the user's shell to `/usr/sbin/nologin` is a strict security measure. It prevents the user from gaining an interactive command-line shell if they attempt to log in via standard SSH. Instead, the connection is immediately closed or rejected, ensuring they can only transfer files via SFTP and cannot execute system commands.

---

## SSH Configuration Explained

### Match Group Snippet:

```ssh
Match Group webadmins
    ChrootDirectory /var/www/main_site
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PasswordAuthentication yes

Match Group menustaff
    ChrootDirectory /var/www/menu_site
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PasswordAuthentication yes
```

### What `ChrootDirectory` Does

`ChrootDirectory` essentially creates a "jail" for the connected user, changing their root directory to the specified path. To the user, `/var/www/main_site` appears as `/` (the top of the file system), making it impossible for them to `cd` up into sensitive system directories like `/etc` or `/var/log`.

### Strict Ownership Requirement

For security, SSH requires that the directory specified in the Chroot directive (the jail itself), and all its parent directories, be owned by `root` and not be group-writable. If this strict `root:root` requirement isn't met, the SSH daemon will refuse the connection entirely.

### What `ForceCommand internal-sftp` Does

Because the user is locked in a jail, they do not have access to standard system binaries (like the regular SFTP server binary usually located in `/usr/lib/`). `ForceCommand internal-sftp` tells the SSH daemon to use its own built-in SFTP server to handle the connection, bypassing the need for external files inside the jail.

---

## Testing & Logs

### Successful SFTP Login

![First screenshot](Picture/3.png)

### Denied SSH Login

![First screenshot](Picture/4.png)

### Log Verification (`/var/log/auth.log`)

This log proves the SSH override successfully allowed password authentication and created the jailed session. The `error: /dev/pts/1: No such file or directory` is definitive proof of the Chroot jail functioning, as the jailed environment lacks standard system device files.

```plaintext
2026-03-25T15:15:22.120017+00:00 ip-10-0-20-196 sshd[1755]: Accepted password for owner from 127.0.0.1 port 48698 ssh2
2026-03-25T15:15:22.121601+00:00 ip-10-0-20-196 sshd[1755]: pam_unix(sshd:session): session opened for user owner(uid=1001) by owner(uid=0)
2026-03-25T15:15:22.128809+00:00 ip-10-0-20-196 systemd-logind[553]: New session 10 of user owner.
2026-03-25T15:15:22.348666+00:00 ip-10-0-20-196 sshd[1840]: error: /dev/pts/1: No such file or directory
```

---

## Permission Verification

### Main Site Directory Status

```plaintext
ubuntu@ip-10-0-20-196:~$ ls -la /var/www/main_site
total 12
drwxr-xr-x 3 root root 4096 Mar 25 14:52 .
drwxr-xr-x 7 root root 4096 Mar 25 14:52 ..
drwxrwxr-x 2 root root 4096 Mar 25 14:52 public_html

ubuntu@ip-10-0-20-196:~$ ls -la /var/www/main_site/public_html
total 8
drwxrwxr-x 2 owner webadmins 4096 Mar 25 14:52 .
drwxr-xr-x 3 root root 4096 Mar 25 14:52 ..
```

### Menu Site Directory Status

```plaintext
ubuntu@ip-10-0-20-196:~$ ls -la /var/www/menu_site
total 12
drwxr-xr-x 3 root         root      4096 Mar 25 14:52 .
drwxr-xr-x 7 root         root      4096 Mar 25 14:52 ..
drwxrwxr-x 2 staff-member menustaff 4096 Mar 25 14:52 public_html

ubuntu@ip-10-0-20-196:~$ ls -la /var/www/menu_site/public_html
total 8
drwxrwxr-x 2 staff-member menustaff 4096 Mar 25 14:52 .
drwxr-xr-x 3 root         root      4096 Mar 25 14:52 ..
```

---

## Explanation of Jail and Edit Permissions

To satisfy the strict requirements of the SSH Chroot feature, the parent jail directories (`/var/www/main_site` and `/var/www/menu_site`) are owned by `root:root` with `755` permissions.

Inside the jails, the `public_html` directories are owned by the specific users (`owner` and `staff-member`) and their corresponding groups (`webadmins` and `menustaff`) with `775` permissions.

This allows members of those groups to freely upload, edit, and delete files inside the web root, while the "other" read/execute permission (the `5` in `775`) ensures the `www-data` service (Apache/Nginx) can still read and serve the files to the public internet.

---
