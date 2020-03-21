# Firewall Rule Proposals

TODO:
- Define SOURCE or DESTINATION as appropriate
- Define PORT and PROTOCOL (say ALL if ALL)
- Define where to place rule 
  - NACL = Network Access Control List
  - SG = Security Group
  - SYS = System level (iptables)
- Define if rule should be INBOUND or OUTBOUND

---

1. Block 203.0.113.5 from reaching any resource in the subnets.
    - SOURCE: 203.0.113.5/32
    - PORTS = ALL
    - PROTOCOLS = ALL
    - NACL INBOUND (Action: DENY)
