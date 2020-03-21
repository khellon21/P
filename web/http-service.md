# NGINX HTTP Web Service Configuration

## Description
This document outlines the setup and configuration of an NGINX web server hosting two distinct websites on an AWS instance. The first is a publicly accessible main website, and the second is a private, isolated site intended only for local TV menu screens.

## Service Configurations

### Key Pieces of a Server Block
In NGINX, a "server block" acts as a virtual host, allowing one server to host multiple sites. Key configuration lines include:
* **`listen`**: Defines the port the site operates on. The main site uses port `80` (standard HTTP), while the menu site uses `8080` to keep it separate from standard web traffic.
* **`server_name`**: The domain name that routes traffic to this specific block (e.g., `patel.wsukduncan.com` and `something-menu.com`).
* **`root`**: The document root, which tells NGINX the exact directory pathway where the website's files are stored (e.g., `/var/www/main` and `/var/www/menu`).

### Enabling and Disabling Sites
In Debian/Ubuntu-based NGINX setups, configuration files are created in `/etc/nginx/sites-available/`. 
* **To enable:** Create a symbolic link of the config file into `/etc/nginx/sites-enabled/` using the command: `sudo ln -s /etc/nginx/sites-available/sitename /etc/nginx/sites-enabled/`.
* **To disable:** Remove the symbolic link from the `sites-enabled` directory using `sudo rm /etc/nginx/sites-enabled/sitename`.

### Restarting the Service
Whenever a configuration file is modified, a new site is enabled, or a site is disabled, the NGINX service must be restarted to apply the changes. Before restarting, it is best practice to test the syntax with `sudo nginx -t`.
* Command to restart: `sudo systemctl restart nginx`

## Name Configurations

* **`patel.wsukduncan.com`**: This name works via standard public DNS records. When a user requests this URL, global DNS resolves it to the server's public IP address, allowing anyone on the internet to view the main site. (Note: For testing purposes on the server itself, this was mapped locally in `/etc/hosts` to bypass the AWS firewall).
* **`something-menu.com`**: This is a localized domain. It works because it was manually added to the server's `/etc/hosts` file and mapped to `127.0.0.1` (localhost). This bypasses public DNS, forcing the server to route requests for this name locally. Combined with a custom port (8080), it ensures only internal systems pointing to that exact host combo can access the menu.

## Screenshots
`curl patel.wsukduncan.com`

![First screenshot](Picture/1.png)

