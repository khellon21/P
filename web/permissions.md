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

