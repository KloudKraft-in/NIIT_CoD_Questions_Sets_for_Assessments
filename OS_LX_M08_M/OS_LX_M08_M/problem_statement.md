# Linux Lab: Network Socket Diagnostics, Routing Path & DNS Troubleshooting (Local VM)

Duration : 90 Min.

## Scenario

A multi-tier web application server is unable to communicate with its backend payment API host. The developer insists 'the network is down'. You must systematically use Linux network diagnostic tools (ss, netstat, traceroute, nslookup, nc) to differentiate whether the fault is a local bind failure, a DNS resolution failure, a gateway routing break, or a remote firewall port block.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Verify whether local services

- Verify whether local services are listening on port 8080 and 443 using ss -tulpn.

### 2. Test DNS resolution of

- Test DNS resolution of api.paymentpartner.internal using nslookup and dig, checking A records.

### 3. Trace the network routing

- Trace the network routing hops to the destination gateway using traceroute -n.

### 4. Perform a TCP socket

- Perform a TCP socket connection test against the remote API port 8443 using nc -zv -w 3.

### 5. Differentiate whether packets are

- Differentiate whether packets are dropped (firewall block) or rejected (connection refused).

### 6. Check local iptables /

- Check local iptables / ufw firewall rules for outgoing drops.

### 7. Test remote latency using

- Test remote latency using ping and analyze packet loss statistics.

### 8. Produce a definitive Network

- Produce a definitive Network Triage Verdict report in ~/network_triage_verdict.json.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Socket state inspection: ss -tulpn correctly captures all listening TCP/UDP sockets | 2 Marks |
| **TC2** | DNS resolution analysis: forward lookup and DNS query response time recorded | 2 Marks |
| **TC3** | Path hop tracing: traceroute output captures the exact hop where latency climbs or drops | 2 Marks |
| **TC4** | Port probe testing: nc -zv accurately identifies port reachability status | 3 Marks |
| **TC5** | Failure signature classification: correctly distinguishes 'Connection Refused' vs 'Connection Timed Out' | 3 Marks |
| **TC6** | Firewall audit: local iptables/nftables rules audited for outbound restrictions | 2 Marks |
| **TC7** | ICMP latency check: ping packet loss and RTT variance documented | 3 Marks |
| **TC8** | Final verdict report: network_triage_verdict.json contains root cause category (DNS, ROUTING, FIREWALL, or SERVICE_DOWN) | 3 Marks |

**Total Score: 20 Marks**
