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

2. Block customers devices from talking to servers.
    - SOURCE: 10.0.0.0/24
    - PORTS = ALL
    - PROTOCOLS = ALL
    - NACL OUTBOUND to SERVER subnet
    - TODO - DESIGN CHANGE - we need NACL to apply unique to subnets

3. Allow HTTP/S traffic from the entire internet to the Web Server.
    - SOURCE: 0.0.0.0/0
    - PORTS = 80 & 443
    - PROTOCOLS = HTTP and HTTPS (TCP)
