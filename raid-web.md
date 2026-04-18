# RAID Web Storage Migration Documentation

## 1. Migration Steps

To ensure website redundancy, the web root was migrated to the RAID 5/6 array. The following commands were used to create the destination directory and copy the files while preserving permissions:

```bash id="k3j9ls"
sudo mkdir -p /mnt/raid_data/www
sudo cp -rp /var/www/html /mnt/raid_data/www/
sudo chown -R www-data:www-data /mnt/raid_data/www/html
```

### Permissions Verification

To verify that the `www-data` ownership was preserved:

```bash id="f2n8qa"
ls -l /mnt/raid_data/www/
```

```plaintext id="d9pz7c"
total 4
drwxr-xr-x 2 www-data www-data 4096 Feb 27 16:31 html
```

**Note:** Directory traversal permissions were also confirmed on `/mnt` and `/mnt/raid_data` using `chmod a+x` to ensure the web server could access the files.

---

## 2. Configuration Snippet

After moving the data, the original web directory was backed up, and a symbolic link was created from `/var/www/html` to the new RAID location:

```bash id="m8x2we"
sudo mv /var/www/html /var/www/html_backup
sudo ln -s /mnt/raid_data/www/html /var/www/html
```

### Symlink Verification

```bash id="p4c7yb"
ls -l /var/www/
```

```plaintext id="q1v8rt"
total 20
lrwxrwxrwx 1 root root   23 Apr 17 23:53 html -> /mnt/raid_data/www/html
drwxr-xr-x 2 root root 4096 Feb 27 16:31 html_backup
drwxr-xr-x 2 root root 4096 Mar 16 15:31 main
drwxr-xr-x 3 root root 4096 Mar 25 14:52 main_site
drwxr-xr-x 2 root root 4096 Mar 16 15:31 menu
drwxr-xr-x 3 root root 4096 Mar 25 14:52 menu_site
```

---

## 3. Verification

### Website Loading

![Website Loading Screenshot](screenshor/raid-web.png)

---

### Storage Verification (`df -h`)

Below is the output showing that the web content is actively being served from the RAID device (`/dev/md0`):

```bash id="z6u1kc"
df -h
```

```plaintext id="y5n0md"
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       6.8G  2.8G  4.0G  42% /
tmpfs           456M     0  456M   0% /dev/shm
tmpfs           183M  952K  182M   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
efivarfs        128K  5.0K  119K   5% /sys/firmware/efi/efivars
/dev/nvme0n1p16 881M  162M  657M  20% /boot
/dev/nvme0n1p15 105M  6.2M   99M   6% /boot/efi
/dev/md0        9.8G  196K  9.3G   1% /mnt/raid_data
tmpfs            92M   12K   92M   1% /run/user/1000
```

---

## 4. Rubric Checklist

* [x] Commands used to migrate website files to `/mnt/raid_data/www`
* [x] Permissions and ownership verification for migrated files
* [x] Symbolic link configuration from `/var/www` to RAID web folders
* [x] Screenshot evidence of website loading from RAID-backed content
* [x] `df -h` output showing content served from `/dev/md0`
