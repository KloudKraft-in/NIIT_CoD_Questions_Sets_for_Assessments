# DevOps Lab: AWS Distributed Jenkins CI/CD Architecture (Master-Agent Setup)

**Duration:** 30 Minutes

## Scenario

As modern enterprises scale, running all CI/CD tasks on a single central server causes resource contention, performance degradation, and security vulnerabilities. To achieve high availability and scalability, organizations implement a distributed Jenkins architecture. 

In this lab, you are a DevOps engineer tasked with building a distributed Jenkins CI/CD infrastructure on AWS. You will provision two Ubuntu EC2 instances—one as the Jenkins Master and the other as a dedicated Jenkins Agent—configure secure SSH-based communication between them, and configure the Jenkins Master to delegate build jobs exclusively to the Agent node.

---

## Task Objectives

To set up this enterprise infrastructure, you must perform the following objectives:
1. **Provision Infrastructure:** Launch and configure two EC2 instances with appropriate naming conventions and security group rules.
2. **Setup Jenkins Master:** Install Jenkins along with all prerequisites (Java, etc.) on the Master node.
3. **Establish Communication:** Configure SSH keys and verify connectivity between the Master and Agent.
4. **Configure Jenkins Agent:** Register the Agent node in the Jenkins dashboard via SSH agent protocol.
5. **Create & Run Distributed Job:** Configure a Freestyle Jenkins job targeted exclusively at the Agent node and capture the execution output.

---

<div style="page-break-before: always;"></div>

## Requirements

### 1. AWS EC2 Provisioning
- **Jenkins Master Node:**
  - **Instance Name (Tag):** `jenkins-master`
  - **Operating System:** Ubuntu 22.04 LTS
  - **Security Group Ports:** 
    - Inbound: SSH (`22`) from your IP, Custom TCP (`8080`) from Anywhere (for Jenkins Dashboard access).
- **Jenkins Agent Node:**
  - **Instance Name (Tag):** `jenkins-agent`
  - **Operating System:** Ubuntu 22.04 LTS
  - **Security Group Ports:** 
    - Inbound: SSH (`22`) from the Jenkins Master's Private IP (or Anywhere for testing purposes).

### 2. Jenkins Master Installation & Setup
- Install **Java Runtime Environment (JRE/JDK)** (recommended version: Java 17 or Java 11) on `jenkins-master`.
- Install **Jenkins** on `jenkins-master`, start the service, and verify it is running.
- Access the Jenkins Dashboard at `http://<jenkins-master-public-ip>:8080` and perform the initial setup (unlock Jenkins and create an admin user).

### 3. SSH Connectivity & Prerequisites on Agent
- Install **Java Runtime Environment (JRE/JDK)** on `jenkins-agent` (must match the Java version installed on the Master).
- Generate an SSH Key Pair on `jenkins-master` (as the `jenkins` user or `ubuntu` user with appropriate permissions).
- Append the public key of the Master to the `/home/ubuntu/.ssh/authorized_keys` file on `jenkins-agent`.
- Verify that `jenkins-master` can successfully SSH into `jenkins-agent` without a password prompt.

<div style="page-break-before: always;"></div>

### 4. Configure Agent Node in Jenkins Dashboard
- Navigate to the Jenkins Dashboard: **Manage Jenkins** -> **Nodes** -> **New Node**.
- Configure the agent with the following details:
  - **Node Name:** `jenkins-agent`
  - **Type:** Permanent Agent
  - **Remote root directory:** `/home/ubuntu/jenkins-agent` (Ensure this directory exists on the agent node)
  - **Labels:** `build-agent`
  - **Launch method:** Launch agents via SSH
  - **Host:** `<jenkins-agent-private-ip>` (or public IP if private IP is not routeable, private IP is recommended for enterprise setups)
  - **Credentials:** Add SSH username (`ubuntu`) and Private Key (private key generated on Master or the SSH private key used to connect).
  - **Host Key Verification Strategy:** Non-verifying Verification Strategy (or Manually Trusted Key Verification Strategy).
- Launch the agent and ensure it shows as **Online** on the Nodes dashboard.

### 5. Freestyle Build Job Configuration
- Create a new Freestyle project in Jenkins named `Agent-Build-Job`.
- Restrict where this project can be run by checking **"Restrict where this project can be run"** and set the **Label Expression** to `build-agent`.
- Under the **Build Steps**, add an **Execute shell** step that runs the following script to generate build details:

```bash
mkdir -p /home/ubuntu/build-logs
echo "--- Execution Details ---" > /home/ubuntu/build-logs/agent-build.log
echo "Build Executed On Node: $(hostname)" >> /home/ubuntu/build-logs/agent-build.log
echo "System OS Info: $(uname -a)" >> /home/ubuntu/build-logs/agent-build.log
echo "Execution Timestamp: $(date)" >> /home/ubuntu/build-logs/agent-build.log
```

- Trigger the build manually.
- Verify in the **Console Output** of the build that the execution happened on `jenkins-agent`.
- Verify the file `/home/ubuntu/build-logs/agent-build.log` is successfully created on the `jenkins-agent` instance and contains the correct execution details.

---

<div style="page-break-before: always;"></div>

## Expected Workflow

```text
       Developer Access
              |
              v
+---------------------------+
|      jenkins-master       | (Port 8080)
|     (Jenkins Master)      |
+-------------+-------------+
              |
              | SSH Connection (Port 22)
              v
+---------------------------+
|       jenkins-agent       | (Executes Freestyle Job)
|      (Jenkins Agent)      | ----> Generates logs at /home/ubuntu/build-logs/agent-build.log
+---------------------------+
```

---

## Sample Evaluation Logs / Output

When checking the console output of your Freestyle job in Jenkins, it should state:
```text
Building remotely on jenkins-agent (build-agent) in workspace /home/ubuntu/jenkins-agent/workspace/Agent-Build-Job
[Agent-Build-Job] $ /bin/sh -xe /tmp/jenkins123456789.sh
+ mkdir -p /home/ubuntu/build-logs
+ echo --- Execution Details ---
+ hostname
+ uname -a
+ date
Finished: SUCCESS
```

The content of the generated file `/home/ubuntu/build-logs/agent-build.log` on the `jenkins-agent` node should look similar to:
```text
--- Execution Details ---
Build Executed On Node: ip-172-31-0-100
System OS Info: Linux ip-172-31-0-100 6.2.0-1017-aws #17~22.04.1-Ubuntu SMP UTC 2026 x86_64 GNU/Linux
Execution Timestamp: Wed Jun 17 12:00:00 UTC 2026
```

---

<div style="page-break-before: always;"></div>

## Deliverables

The final implementation must consist of:

| Deliverable | Description |
| :--- | :--- |
| **Jenkins Master Server** | Running Ubuntu EC2 instance named `jenkins-master` with Jenkins running on port 8080. |
| **Jenkins Agent Server** | Running Ubuntu EC2 instance named `jenkins-agent` connected to Master. |
| **Active SSH Connection** | Passwordless key-based SSH authorization established between master and agent. |
| **Configured Jenkins Node** | An online permanent agent node configured in Jenkins Dashboard named `jenkins-agent`. |
| **Freestyle Build Job** | Jenkins job named `Agent-Build-Job` configured with the label restriction. |
| **Verification Build Log** | A log file located at `/home/ubuntu/build-logs/agent-build.log` on `jenkins-agent` proving successful remote build execution. |

---

## Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Amazon EC2** | Compute instances for Master and Agent environments. |
| **Ubuntu Linux** | Server OS for host VM environments. |
| **Jenkins** | CI/CD Server orchestrating builds. |
| **SSH (Port 22)** | Protocol for remote execution and Jenkins agent launching. |
| **Java 11 / 17** | Required runtime engine for Jenkins Master and Agent nodes. |

---

<div style="page-break-before: always;"></div>

## Verification & Grading Criteria

Your configuration will be automatically graded based on the following verification checks:

| Test Case | Requirement | Validation Method | Marks |
| :--- | :--- | :--- | :--- |
| **TC1** | **EC2 Instancing & Basic Settings** | Verifies that two running instances named `jenkins-master` and `jenkins-agent` exist with correct security group rules. | 5 Marks |
| **TC2** | **Jenkins Master Installation** | Verifies that the Jenkins service is active and running on `jenkins-master` and accessible via HTTP port 8080. | 5 Marks |
| **TC3** | **Distributed Node Configuration** | Verifies that `jenkins-agent` is registered as a node in Jenkins and is in the "Online" state. | 5 Marks |
| **TC4** | **Freestyle Job & Agent Build Log** | Verifies that `Agent-Build-Job` exists, ran on `jenkins-agent`, and wrote the build log to `/home/ubuntu/build-logs/agent-build.log`. | 5 Marks |

**Total Score: 20 Marks**

---

## Optional Enhancements

For additional practice, learners may attempt to implement:
- Setup agent node auto-scaling using AWS EC2 plugins.
- Secure Jenkins using SSL/HTTPS via an Nginx Reverse Proxy.
- Configure Jenkins credentials using HashiCorp Vault.
- Containerize the Jenkins Agent using Docker-based agents.
- Configure notifications (Slack or Email) on successful build executions.

---

## Real-World Use Case

Distributed CI/CD architectures are standard industry practice to ensure that resource-intensive workflows (like compilation, testing, and container builds) do not starve the Jenkins control plane of CPU or memory, which could disrupt the entire development organization. Setting up secure, SSH-based agent scaling represents the foundational skill needed to manage distributed clouds, hybrid architectures, and elastic build clusters in enterprise environments.
