[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/JyInQUes)
## Lab 5 - NIST : CEG 3400

### NIST Vulnerability Taxonomies

#### Name: Khellon Patel

### Task 1 - Inventory

* Your 5 CPE's that describe your laptop's software environment.  Please include an OS, web browser, and 3 other valid CPE's for software on your laptop (ideally related to school). 
  * **Operating System:** `cpe:2.3:o:linux:acrn:1.3:*:*:*:*:*:*:*`
  * **Web Browser:** `cpe:2.3:a:google:chrome:0.3.154.0:*:*:*:*:*:*:*`
  * **CS/CEG/IT Software 1:** `cpe:2.3:a:apple:afp_server:-:*:*:*:*:*:*:*`
  * **CS/CEG/IT Software 2:** `cpe:2.3:a:agendaless:pyramid:1.0:beta3:*:*:*:python:*:*`
  * **Personal/Wildcard Software:** `cpe:2.3:a:cogboard:red_discord_bot:3.2.2:*:*:*:*:*:*:*`

---

### Task 2 - Your (not real) CPE

* Your properly formatted CPE:
  `cpe:2.3:a:khellon_patel:split_guys:1.0.0:*:*:*:*:*:*:*`

Explanation:
* **Part (`a`):** Selected `a` because "Split Guys" is a software application, not hardware (`h`) or an operating system (`o`).
* **Vendor (`khellon_patel`):** Identifies the creator and maintainer responsible for the software.
* **Product (`split_guys`):** Specifies the exact name of the software package.
* **Version (`1.0.0`):** Adheres to Semantic Versioning (SemVer 2.0.0), indicating the first major, stable release of the software where the vulnerability was present.
* **Wildcards (`*`):** Used the wildcard character `*` for the remaining fields (update, edition, language, sw_edition, target_sw, target_hw, and other). The weakness exists in the core application logic (the backend code), meaning the vulnerability affects all users regardless of their operating system, device hardware, or language settings. 

---

### Task 3 - CWE

* Link to your top 25 CWE
  [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)

Description:
SQL Injection occurs when a software application takes untrusted input from a user and inserts it directly into a backend database query without properly sanitizing it or using parameterized queries. This allows an attacker to manipulate the input to change the logic of the SQL statement. A well-known example of this is **CVE-2023-34362**, a massive vulnerability discovered in the MOVEit file transfer software, which allowed unauthenticated attackers to gain unauthorized access to the database.

**My Vulnerable Code & Impact:**
In the "Split Guys" application, I created a search feature that allows users to filter their past expenses by typing in a category name (e.g., "Groceries"). In the backend, I concatenated the user's search string directly into the database query: `SELECT * FROM expenses WHERE category = '` + userInput + `';`. Because this code does not sanitize the input, an attacker could enter a payload like `' OR '1'='1` into the search bar. The database would ignore the category filter and return every single row in the `expenses` table, completely compromising the confidentiality of all user financial records.

---

### Task 4 - CVE

* List your properly formatted CVE here:
  **CVE-2024-XXXXX (Pending)**
  **CNA:** Matt Kijowski

* Assign a CVSS score and defend it (why did you select what you selected in the calculator)
  * **Base Score:** 9.8 (Critical)
  * **Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
  * **Defense/Justification:** * **Attack Vector (Network):** The application is web-facing, allowing the attack to be executed remotely over the internet.
    * **Attack Complexity (Low):** Exploiting the unsanitized search bar requires no special access conditions; a standard SQL injection payload is trivial to execute.
    * **Privileges Required (None):** The expense search feature is accessible without needing to log in or hold an administrative account.
    * **User Interaction (None):** The attacker executes the payload directly; no victim needs to click a link or download a file.
    * **Scope (Unchanged):** The vulnerable component and the impacted component (the database) are under the same security authority.
    * **Confidentiality, Integrity, & Availability (High):** A successful injection allows the attacker to read all private data (Confidentiality), modify or manipulate records (Integrity), and drop entire database tables (Availability).

CVE writeup:
A vulnerability in the expense search module of Khellon Patel Split Guys v1.0.0 allows unauthenticated remote attackers to execute arbitrary SQL commands via improper neutralization of user-supplied input (SQL Injection). This leads to unauthorized data access and potential database destruction. The root cause is the concatenation of raw, unsanitized user input directly into SQL `SELECT` statements instead of utilizing prepared statements. 

**References:**
* https://github.com/yourusername/CEG3400-Lab5-repo
