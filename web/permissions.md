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

