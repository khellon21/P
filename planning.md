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
