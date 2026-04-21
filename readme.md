# Assignment: The Digital Phonebook (Intro to LDAP)

This project sets up a small OpenLDAP directory for the fictional domain
`class.local` (base DN: `dc=class,dc=local`). It demonstrates a
centralized "source of truth" for user accounts.

## Files

### structure.ldif
Defines the two Organizational Units (OUs) that act as "folders" inside
the directory tree:

- `ou=People` — container for all user account entries.
- `ou=Groups` — container for group entries (e.g., posixGroup objects
  later on).

Each OU uses the `organizationalUnit` objectClass, which is the standard
LDAP class for grouping entries.

### users.ldif
Populates `ou=People` with two user accounts. Each entry combines three
objectClasses so the user is usable across different systems:

- `inetOrgPerson` — standard person attributes (sn, givenName, cn, mail).
- `posixAccount` — Unix/Linux login attributes (uidNumber, gidNumber,
  homeDirectory, loginShell) so the same record can authenticate SSH
  logins.
- `shadowAccount` — password aging attributes for shadow-password
  compatibility.

The two accounts created are:
1. `uid=khellon` — my own account.
2. `uid=testuser` — a test account to confirm multiple users are
   searchable.

## How to reproduce

See the command guide below (Parts 1–4).

## Screenshots
- `screenshot-01-ous.png` — `ldapsearch` output showing both OUs.
- `screenshot-02-user.png` — `ldapsearch` output showing my user entry.

## Written Response
See the final section.
