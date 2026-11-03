# Linux Lab: Network Interface Configuration via nmcli & Headless Connectivity (Local VM)

Duration : 30 Min.

## Scenario

A headless enterprise server has lost network connectivity after an automated configuration drift. With no GUI available, you must utilize the `nmcli` command-line utility to reconfigure interface `eth1` with a static IPv4 address, default gateway, and DNS servers, and activate the connection profile without disrupting existing management interfaces.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Inspect current network devices

- Ensure the target lab interface is initialized by bringing up the dedicated `eth1` interface (e.g. `sudo ip link add eth1 type veth peer name eth1_peer 2>/dev/null || sudo ip link add eth1 type dummy 2>/dev/null && sudo ip link set eth1 up`).
- Inspect current network devices and connection profiles using `nmcli device status` and `nmcli connection show`.
- Save your device inspection output to `~/network_devices.txt` (e.g., `nmcli device status > ~/network_devices.txt`).

### 2. Modify connection profile 'static-eth1'

- Configure the NetworkManager connection profile `static-eth1` to bind to interface `eth1`.
- Set IPv4 configuration method to `manual`.
- Assign static IPv4 address `192.168.10.50/24`.
- Configure default gateway `192.168.10.1`.
- Configure DNS server `8.8.8.8`.

### 3. Bring up the connection

- Bring up and activate the connection using `nmcli connection up static-eth1`.
- Ensure the connection activates successfully and binds the static IP to `eth1`.

### 4. Verify routing table entry and reachability

- Verify routing table entries via `ip route show` and save output to `~/ip_route.txt`.
- Verify the IP address assignment with `ip addr show eth1`.
- Test reachability of the default gateway (`192.168.10.1`).

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score:
```bash
python3 student_workspace/run.py
```

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Device identification: nmcli correctly identifies target ethernet interface eth1 | 2 Marks |
| **TC2** | Static IP configuration: static-eth1 profile configured with correct IPv4 CIDR and manual method | 3 Marks |
| **TC3** | Gateway and DNS: default gateway and DNS servers successfully written to connection settings | 3 Marks |
| **TC4** | Profile activation: nmcli connection up succeeds and IP address binds to interface | 2 Marks |

**Total Score: 10 Marks**
