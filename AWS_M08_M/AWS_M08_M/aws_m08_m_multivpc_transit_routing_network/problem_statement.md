# AWS Lab: Multi-VPC Transit Routing & Network Firewall Packet Drop Triage

Duration : 90 Min.

## Scenario
A newly deployed microservice in VPC-A (10.1.0.0/16) cannot communicate with a backend database in VPC-B (10.2.0.0/16) across an AWS Transit Gateway. Traffic reaches the Transit Gateway but receives no response. The engineer must conduct a multi-layer network audit across: (1) VPC-A Route Table (missing route to 10.2.0.0/16 via tgw-xxx), (2) VPC-B Network ACL (inbound ephemeral ports blocked), and (3) Database Security Group (missing ingress rule from 10.1.0.0/16). The engineer must resolve all three network layers to restore end-to-end connectivity.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** AWS Transit Gateway & Multi-VPC Networking
- **VPC CIDRs:** VPC-A (`10.1.0.0/16`) to VPC-B Database (`10.2.0.0/16`, port 5432)
- **Defects:** (1) Missing route in VPC-A route table, (2) Stateless NACL blocking ephemeral return ports (1024-65535), (3) SG missing ingress

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Ingest multi-VPC configuration files from /opt/aws_net/transit_topology.json.
2. Audit VPC-A subnet route tables: detect missing route to 10.2.0.0/16.
3. Audit VPC-B Network ACLs: identify stateless NACL blocking return traffic on ephemeral ports (1024-65535).
4. Audit Database Security Group: identify missing ingress rule for port 5432 from 10.1.0.0/16.
5. Formulate remediation script ~/remediate_transit_routing.sh adding the route, updating the NACL, and modifying the Security Group.
6. Execute end-to-end packet flow verification script testing TCP socket connectivity on port 5432.
7. Output complete network topology sign-off report to ~/transit_network_signoff.json.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Multi-layer inspection: systematically audit Route Tables, NACLs, and Security Groups | 3 Marks |
| **TC2** | Route table correction: add route 10.2.0.0/16 targeting Transit Gateway in VPC-A route table | 3 Marks |
| **TC3** | Stateless NACL correction: explain and fix NACL return traffic drop on ephemeral ports | 3 Marks |
| **TC4** | Security group ingress: authorize port 5432 ingress restricted to VPC-A CIDR block | 3 Marks |
| **TC5** | Remediation script: remediate_transit_routing.sh executes all AWS CLI commands idempotently | 3 Marks |
| **TC6** | Connectivity verification: verify TCP handshake establishes successfully between VPC-A and VPC-B | 3 Marks |
| **TC7** | Topology sign-off: transit_network_signoff.json documents all resolved network hops | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
