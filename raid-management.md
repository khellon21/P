# RAID Array Configuration & Management

---

## 1. Architecture Choice

* **Level Chosen:** RAID 5

* **Reasoning:**
  I chose RAID 5 because it offers a good balance between usable storage capacity and fault tolerance. It requires a minimum of 3 drives and can withstand the failure of 1 drive. While RAID 6 offers higher fault tolerance (surviving 2 drive failures), it requires more drives and sacrifices more overall storage capacity to double parity.

---

## 2. Storage Math

* **Formula for RAID 5 Usable Space:**
  `(n - 1) * S`
  *(where `n` is the number of disks and `S` is the size of the smallest disk)*

* **My Array:**
  Three 5 GiB drives

* **Calculation:**
  `(3 - 1) * 5 GiB = 10 GiB` usable space

---

## 3. Configuration Snippets

### Creation Command

```bash
sudo mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/nvme1n1 /dev/nvme2n1 /dev/nvme3n1
```

### Array Clean State (`mdadm --detail`)

```text
ubuntu@ip-10-0-20-196:~$ sudo mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Mon Mar 30 15:32:00 2026
        Raid Level : raid5
        Array Size : 10475520 (9.99 GiB 10.73 GB)
     Used Dev Size : 5237760 (5.00 GiB 5.36 GB)
      Raid Devices : 3
     Total Devices : 2
       Persistence : Superblock is persistent

       Update Time : Mon Mar 30 15:42:33 2026
             State : clean, degraded 
    Active Devices : 2
   Working Devices : 2
    Failed Devices : 0
     Spare Devices : 0

            Layout : left-symmetric
        Chunk Size : 512K

Consistency Policy : resync

              Name : ip-10-0-20-196:0  (local to host ip-10-0-20-196)
              UUID : f3e31ddd:a0c25dcd:311fdfc9:96487261
            Events : 21

    Number   Major   Minor   RaidDevice State
       -       0        0        0      removed
       1     259        1        1      active sync   /dev/nvme2n1
       3     259        2        2      active sync   /dev/nvme3n1
ubuntu@ip-10-0-20-196:~$ 

```

### Filesystem Creation

```bash
sudo mkfs.ext4 /dev/md0
```

---

## 4. Persistence Strategy

### `/etc/fstab` Entry

```text
UUID=03d4ae6d-4c32-405d-bcd8-f126e0986cfe  /mnt/raid_data  ext4  defaults  0  0
```

### `/etc/mdadm/mdadm.conf` Contents

```text
ARRAY /dev/md0 metadata=1.2 UUID=f3e31ddd:a0c25dcd:311fdfc9:96487261
```

### Why `mdadm.conf` Is Necessary

This file stores the array’s configuration (blueprint). When the system reboots, Linux reads this file to:

* Identify which physical disks belong to `/dev/md0`
* Reassemble the RAID array correctly
* Ensure the filesystem mounts properly via `/etc/fstab`

Without this file, the array may not assemble automatically during boot.

---

## 5. Failure & Recovery Log

### Failing the Drive

To simulate a failure:

```bash
sudo mdadm --manage /dev/md0 --fail /dev/nvme1n1
```

---

### Removing the Faulty Drive

```bash
sudo mdadm --manage /dev/md0 --remove /dev/nvme1n1
```

---

### Adding a Replacement Drive

After attaching a new 5 GiB volume:

```bash
sudo mdadm --manage /dev/md0 --add /dev/nvmeXn1
```

*(Replace `X` with the correct device letter)*

---

### Rebuild Process

* The array begins rebuilding automatically after adding the new drive.
* You can monitor progress using:

  ```bash
  cat /proc/mdstat
  ```

---

### Rebuild Time

The rebuild took approximately:
**[INSERT YOUR TIME HERE — e.g., 30 seconds / 1 minute]**
![First screenshot](screenshor/task5.png)
---

**End of Document**
