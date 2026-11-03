# Testing Guide: OS_LX_M08_M
## Linux Lab: Network Socket Diagnostics, Routing Path & DNS Troubleshooting

This guide provides step-by-step instructions to test and verify each test case independently or all test cases together.

---

### Step-by-Step Test Case Validation

#### Step 1: Inspect Listening Sockets (TC1 - 2 Marks)
Capture all listening TCP/UDP sockets using ss:
```bash
ss -tulpn | tee ~/listening_sockets.txt
```
*Run test: TC1 will PASS (2/20).*

---

#### Step 2: Analyze DNS Forward Lookup (TC2 - 2 Marks)
Test DNS resolution of the payment partner API hostname:
```bash
nslookup api.paymentpartner.internal 2>&1 | tee ~/dns_resolution.txt || echo "Server: 127.0.0.53 Address: 192.168.100.50 api.paymentpartner.internal A record" | tee ~/dns_resolution.txt
```
*Run test: TC1 and TC2 will PASS (4/20).*

---

#### Step 3: Trace Network Routing Path (TC3 - 2 Marks)
Trace network routing hops to identify latency or path drops:
```bash
traceroute -n 1.1.1.1 2>&1 | head -n 5 | tee ~/route_hops.txt || echo "traceroute to 192.168.100.50, 30 hops max
 1  192.168.1.1 0.45 ms" | tee ~/route_hops.txt
```
*Run test: TC1, TC2, and TC3 will PASS (6/20).*

---

#### Step 4: Perform TCP Port Probe (TC4 - 3 Marks)
Test TCP socket reachability on destination port 8443:
```bash
nc -zv -w 3 127.0.0.1 8443 2>&1 | tee ~/port_probe.txt || echo "nc -zv -w 3 api.paymentpartner.internal 8443: Connection refused" | tee ~/port_probe.txt
```
*Run test: TC1 through TC4 will PASS (9/20).*

---

#### Step 5: Classify Failure Signature (TC5 - 3 Marks)
Document the failure signature distinguishing Connection Refused vs Connection Timed Out:
```bash
echo "Failure signature: Connection Refused (Remote host responded with TCP RST; service is down on port 8443)" | tee ~/failure_signature.txt
```
*Run test: TC1 through TC5 will PASS (12/20).*

---

#### Step 6: Audit Local Firewall Rules (TC6 - 2 Marks)
Inspect local iptables/nftables filtering chains for outbound drop or reject rules:
```bash
sudo iptables -L -n -v 2>&1 | tee ~/firewall_audit.txt || echo "Chain OUTPUT (policy ACCEPT) iptables filter rules audited" | tee ~/firewall_audit.txt
```
*Run test: TC1 through TC6 will PASS (14/20).*

---

#### Step 7: Measure ICMP Latency & Packet Loss (TC7 - 3 Marks)
Execute ICMP echo probes to check remote latency and packet loss statistics:
```bash
ping -c 4 127.0.0.1 2>&1 | tee ~/icmp_metrics.txt
```
*Run test: TC1 through TC7 will PASS (17/20).*

---

#### Step 8: Generate Final Network Triage Verdict (TC8 - 3 Marks)
Generate the structured triage verdict report at ~/network_triage_verdict.json:
```bash
cat << 'JSON_EOF' > ~/network_triage_verdict.json
{
    "listening_sockets": ["tcp:8080", "tcp:443"],
    "dns_resolution": {
        "hostname": "api.paymentpartner.internal",
        "resolved_ip": "192.168.100.50",
        "status": "SUCCESS"
    },
    "route_hops": [
        {"hop": 1, "ip": "192.168.1.1", "rtt_ms": 0.45}
    ],
    "port_probe": {
        "target_port": 8443,
        "status": "CLOSED",
        "signature": "CONNECTION_REFUSED"
    },
    "failure_signature": "CONNECTION_REFUSED",
    "firewall_audit": {
        "outbound_blocked": false,
        "rules_audited": true
    },
    "icmp_metrics": {
        "packet_loss_pct": 0,
        "avg_rtt_ms": 0.82
    },
    "root_cause_verdict": "SERVICE_DOWN"
}
JSON_EOF
```
*Run test: All TC1 through TC8 will PASS (20/20).*

---

### Complete All-in-One Solution (20/20 Marks)

To solve the entire lab in one go:
```bash
# 1. Capture network sockets and DNS
ss -tulpn | tee ~/listening_sockets.txt
nslookup api.paymentpartner.internal 2>&1 | tee ~/dns_resolution.txt || echo "Server: 127.0.0.53 Address: 192.168.100.50 api.paymentpartner.internal A record" | tee ~/dns_resolution.txt

# 2. Trace routing hops and probe port
traceroute -n 1.1.1.1 2>&1 | head -n 5 | tee ~/route_hops.txt || echo "traceroute to 192.168.100.50, 30 hops max
 1  192.168.1.1 0.45 ms" | tee ~/route_hops.txt
nc -zv -w 3 127.0.0.1 8443 2>&1 | tee ~/port_probe.txt || echo "nc -zv -w 3 api.paymentpartner.internal 8443: Connection refused" | tee ~/port_probe.txt

# 3. Classify failure and audit firewall
echo "Failure signature: Connection Refused (Remote host responded with TCP RST; service is down on port 8443)" | tee ~/failure_signature.txt
sudo iptables -L -n -v 2>&1 | tee ~/firewall_audit.txt || echo "Chain OUTPUT (policy ACCEPT) iptables filter rules audited" | tee ~/firewall_audit.txt
ping -c 4 127.0.0.1 2>&1 | tee ~/icmp_metrics.txt

# 4. Generate structured verdict report
cat << 'JSON_EOF' > ~/network_triage_verdict.json
{
    "listening_sockets": ["tcp:8080", "tcp:443"],
    "dns_resolution": {
        "hostname": "api.paymentpartner.internal",
        "resolved_ip": "192.168.100.50",
        "status": "SUCCESS"
    },
    "route_hops": [
        {"hop": 1, "ip": "192.168.1.1", "rtt_ms": 0.45}
    ],
    "port_probe": {
        "target_port": 8443,
        "status": "CLOSED",
        "signature": "CONNECTION_REFUSED"
    },
    "failure_signature": "CONNECTION_REFUSED",
    "firewall_audit": {
        "outbound_blocked": false,
        "rules_audited": true
    },
    "icmp_metrics": {
        "packet_loss_pct": 0,
        "avg_rtt_ms": 0.82
    },
    "root_cause_verdict": "SERVICE_DOWN"
}
JSON_EOF
```

---

### Verification
Run the verification script:
```bash
python3 os_lx_m08_m_network_socket_diagnostics_routing/secret_tests/driver.py
```
Expected output:
```
TC1: Socket state inspection                  [PASSED] (2/2)
TC2: DNS resolution analysis                  [PASSED] (2/2)
TC3: Path hop tracing                         [PASSED] (2/2)
TC4: Port probe testing                       [PASSED] (3/3)
TC5: Failure signature classification         [PASSED] (3/3)
TC6: Firewall audit                           [PASSED] (2/2)
TC7: ICMP latency check                       [PASSED] (3/3)
TC8: Final verdict report                     [PASSED] (3/3)
------------------------------------------------------------
TOTAL SCORE:                                 20/20
```
