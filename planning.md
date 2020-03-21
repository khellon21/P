# Web Hosting - Planning Phase

## 1. Stack Identification
* **Assigned Stack:** [Select one: Apache HTTP Server (Door Side) | Nginx (Non-Door Side)]
* **Operating System:** [e.g., Ubuntu 24.04 LTS]

---

## 2. Infrastructure & Ports
### Port Requirements
| Direction | Port | Protocol | Source/Destination | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Inbound** | 80 | TCP | 0.0.0.0/0 (Anywhere) | Standard HTTP Traffic |
| **Inbound** | 443 | TCP | 0.0.0.0/0 (Anywhere) | Secure HTTPS Traffic |
| **Inbound** | 22 | TCP | Admin IP / Management VPC | SSH Access for Management |
| **Outbound** | 80/443 | TCP | OS Repositories | Software updates and patches |

### Firewall Configuration
* **NACL:** Stateless level. Must allow inbound 80/443 and allow outbound to **ephemeral ports** (1024-65535) to permit return traffic to the client.
* **Security Group (SG):** Stateful level. Rules needed for Inbound 80, 443, and 22. Outbound is typically "Allow All" by default.
* **System Firewall:** * *If Apache:* `sudo ufw allow 'Apache Full'`
    * *If Nginx:* `sudo ufw allow 'Nginx Full'`

---

## 3. Web Service Configuration
### Configuration Files
* **Main Config Path:** [Apache: `/etc/apache2/apache2.conf` | Nginx: `/etc/nginx/nginx.conf`]
* **Virtual Host Path:** [Apache: `/etc/apache2/sites-available/` | Nginx: `/etc/nginx/conf.d/` or `sites-available/`]
* **Additional Mods:** Edit `/etc/hosts` on the local machine to map the server IP to the two test domains (e.g., `192.168.1.10 site1.test site2.test`).

### Service Control (Daemon)
* **Start:** `sudo systemctl start [apache2|nginx]`
* **Stop:** `sudo systemctl stop [apache2|nginx]`
* **Restart:** `sudo systemctl restart [apache2|nginx]`
* **Reload (Config change only):** `sudo systemctl reload [apache2|nginx]`

---

## 4. Location & Access
### Content Organization
* **Root Directory:** `/var/www/`
* **Site 1:** `/var/www/site1/public_html`
* **Site 2:** `/var/www/site2/public_html`

### Permissions & Users
* **Runtime User:** `www-data` (or `nginx`/`apache` depending on OS).
* **Directory Permissions:** `755` (Owner: rwx, Group/Others: r-x).
* **File Permissions:** `644` (Owner: rw-, Group/Others: r--).
* **Developer Access:** **SFTP** (Secure File Transfer Protocol) over SSH. 
* **Dev Permissions:** Developers will be added to the `www-data` group. Use `chmod -R g+s` on web directories so new files inherit group ownership.

---

## 5. Planning for HTTPS
### Certificate Management
* **Creation:** Use OpenSSL: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/webserver.key -out /etc/ssl/certs/webserver.crt`
* **Storage:** * Private Key: `/etc/ssl/private/` (Permission: `600` - Root only).
    * Public Cert: `/etc/ssl/certs/` (Permission: `644`).
* **CA Validation:** **Domain Validation (DV)** is appropriate for this use case as it verifies control over the domain without requiring legal business documentation.

### HTTPS Implementation
* **Virtual Host Changes:** Add a new block/server section listening on port **443** with `ssl` enabled and paths to the `.crt` and `.key` files.
* **HTTP Redirection:** * *Apache:* Use `Redirect permanent / https://[domain]/` inside the port 80 VirtualHost.
    * *Nginx:* Use `return 301 https://$host$request_uri;` inside the port 80 server block.

---

## 6. Logging (Stretch Goals)
* **Log Locations:** `/var/log/[apache2|nginx]/access.log` and `error.log`.
* **Viewing Logs:** `tail -f /var/log/[service]/access.log` for real-time traffic monitoring.
