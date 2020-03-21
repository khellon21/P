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

