# DevOps Lab: AWS Application Load Balancer (ALB) Path-Based Routing

**Difficulty Level:** Medium
**Duration:** 120 Minutes

## Scenario

Your company is deploying a new web platform comprised of three distinct microservices:
- **Service A (Product Catalog):** Serves traffic under the URL path prefix `/app1`.
- **Service B (Order Management):** Serves traffic under the URL path prefix `/app2`.
- **Service C (User Profile):** Serves traffic under the URL path prefix `/app3`.

To ensure high availability and load distribution, each microservice must run on a separate EC2 instance deployed in a different Availability Zone (AZ) within the same AWS region. An Application Load Balancer (ALB) must be positioned in front of these services to serve as the single public entry point, routing requests dynamically to the correct target group based on the HTTP request URL path.

To secure this multi-tier architecture, direct internet access to the EC2 instances must be blocked. The instances must only accept HTTP traffic routed through the ALB.

---

## Task Objectives

To set up this high-availability web architecture, you must perform the following tasks:
1. **Launch 3 EC2 Instances:** Provision three Ubuntu EC2 instances—each in a different Availability Zone (e.g., `a`, `b`, and `c` suffixes)—and name them according to the convention.
2. **Install Web Application Servers:** On each instance, configure a web service (e.g., Nginx, Apache, or Python HTTP server) serving content on port `80` under its corresponding path (`/app1`, `/app2`, or `/app3`).
3. **Provision Application Load Balancer:** Set up a public-facing Application Load Balancer (ALB) across multiple public subnets.
4. **Create Target Groups:** Configure three separate target groups (one for each microservice) with active HTTP health checks.
5. **Configure Path-Based Listener Rules:** Add a listener on port `80` to the ALB with routing rules that direct incoming traffic as follows:
   - Path `/app1*` routes to Target Group A
   - Path `/app2*` routes to Target Group B
   - Path `/app3*` routes to Target Group C
6. **Secure Security Groups:** Restrict the EC2 instances' security group rules to only allow inbound TCP port `80` traffic coming from the ALB's security group.

---

## Requirements

> [!WARNING]
> **CRITICAL RESOURCE CONFIGURATION & NAMING REQUIREMENT:**
> 1. You must name all resources using your **AWS IAM username** as a **prefix** (e.g. if your AWS IAM username is `ltm-devops-user1`, then your VM must be named `ltm-devops-user1-service-a-host`). Do **NOT** use your platform username (e.g. `Niit`) or the default OS user `niit` as the name or suffix. Doing so will cause the VM Validation test case to fail. Note that the ALB and Target Group names must also be prefixed with your AWS IAM username and use the shortened format below to avoid exceeding AWS's 32-character limit (e.g., `<username>-services-alb` and `<username>-tg-app1`).
> 2. You **MUST** attach the IAM role **`Ec2_instance_SSM`** to **all** EC2 instances. This is required for the automated grading tool to verify your local configurations and files via AWS Systems Manager (SSM). Without this role attached, test verification checks will fail.
> 3. You **MUST** use **`t3.micro`** as the instance type for all VMs.

### 1. EC2 Microservice Instances
- **Instance 1 (Service A):**
  - **Name Tag:** `<username>-service-a-host`
  - **Availability Zone:** AZ1 (e.g., `us-east-1a`)
  - **Service Path:** `http://<private-ip>/app1/` (Should return a simple message like "Product Catalog Service")
- **Instance 2 (Service B):**
  - **Name Tag:** `<username>-service-b-host`
  - **Availability Zone:** AZ2 (e.g., `us-east-1b`)
  - **Service Path:** `http://<private-ip>/app2/` (Should return a simple message like "Order Management Service")
- **Instance 3 (Service C):**
  - **Name Tag:** `<username>-service-c-host`
  - **Availability Zone:** AZ3 (e.g., `us-east-1c`)
  - **Service Path:** `http://<private-ip>/app3/` (Should return a simple message like "User Profile Service")

### 2. Application Load Balancer (ALB)
- **ALB Name:** `<username>-services-alb`
- **Scheme:** Internet-facing
- **Listener:** Port `80` (HTTP)
- **Target Groups:**
  - `<username>-tg-app1` (containing `<username>-service-a-host` on port 80)
  - `<username>-tg-app2` (containing `<username>-service-b-host` on port 80)
  - `<username>-tg-app3` (containing `<username>-service-c-host` on port 80)

### 3. Security & Access Control
- **ALB Security Group:** Allows inbound HTTP (`80`) from Anywhere (`0.0.0.0/0`).
- **EC2 Instance Security Group:** Allows inbound HTTP (`80`) only from the **ALB Security Group ID**. It must reject direct HTTP traffic from any other source.

---

## Expected Workflow

```text
               User Requests
                     |
                     v
          +---------------------+
          |   app-services-alb  | (HTTP Port 80)
          +----------+----------+
                     |
         +-----------+-----------+
         |/app1*     |/app2*     |/app3*
         v           v           v
   +-----------+ +-----------+ +-----------+
   | service-a | | service-b | | service-c |
   | (AZ1)     | | (AZ2)     | | (AZ3)     |
   +-----------+ +-----------+ +-----------+
```

---

## Sample Health Check & Routing Responses

When accessing the load balancer via its public DNS name:
- Querying `http://<alb-dns-name>/app1/` should return:
  ```text
  Product Catalog Service - Status: OK
  ```
- Querying `http://<alb-dns-name>/app2/` should return:
  ```text
  Order Management Service - Status: OK
  ```
- Querying `http://<alb-dns-name>/app3/` should return:
  ```text
  User Profile Service - Status: OK
  ```

---

## Deliverables

The final implementation must consist of:

| Deliverable | Description |
| :--- | :--- |
| **Three Running Instances** | EC2 instances named `<your-aws-iam-username>-service-a-host`, `<your-aws-iam-username>-service-b-host`, and `<your-aws-iam-username>-service-c-host` placed in three distinct Availability Zones. |
| **Three Web Applications** | HTTP servers serving the correct content under `/app1/`, `/app2/`, and `/app3/` on the respective hosts. |
| **Application Load Balancer** | Active ALB named `<your-aws-iam-username>-services-alb` configured with target routing rules. |
| **Three Target Groups** | Target groups named `<your-aws-iam-username>-tg-app1`, `<your-aws-iam-username>-tg-app2`, and `<your-aws-iam-username>-tg-app3` configured on port 80 with passing health check metrics. |
| **Secure Instance Security Group** | Instance firewall rules that block direct internet access and permit traffic only from the ALB. |

---

## Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Amazon EC2** | Microservice compute host nodes. |
| **AWS ALB** | Application Load Balancer orchestrating path-based traffic routing. |
| **Security Groups** | Stateful firewalls controlling ingress and egress traffic. |
| **Ubuntu Linux** | Guest operating systems. |
| **Nginx / HTTP daemon** | Web servers hosting the microservice endpoints. |

---

## Verification & Grading Criteria

> [!IMPORTANT]
> VM Creation and Naming validation is strictly enforced. The VM names must exactly match the convention `<username>-service-a-host`, `<username>-service-b-host`, and `<username>-service-c-host`. Creating a VM with an incorrect name or using a suffix/portal username will result in immediate failure of the VM Validation test case, even if the VM is successfully created.

Your infrastructure configuration will be automatically graded based on the following checks:

| Test Case | Requirement | Validation Method | Marks |
| :--- | :--- | :--- | :--- |
| **TC1** | **VM Creation and Naming Validation** | Verifies that all required VMs are created and their names exactly match the expected convention (`<username>-service-a-host`, `<username>-service-b-host`, and `<username>-service-c-host`). | 2 Marks |
| **TC2** | **EC2 Instances Provisioning** | Verifies three EC2 instances exist, are running, and are spread across three distinct AZs. | 3 Marks |
| **TC3** | **Application Load Balancer Setup** | Verifies `<username>-services-alb` is active, has a public DNS name, and is listening on port 80. | 3 Marks |
| **TC4** | **Target Groups & Path Routing** | Verifies three target groups (`<username>-tg-app1`, `<username>-tg-app2`, `<username>-tg-app3`) are configured with path-based listener rules forwarding `/app1*`, `/app2*`, and `/app3*` correctly. | 4 Marks |
| **TC5** | **Security Group Restrictions** | Verifies instances block direct internet access and only allow inbound HTTP port 80 traffic from the ALB. | 4 Marks |
| **TC6** | **End-to-End Routing & Health Status** | Verifies targets show as healthy and requesting the paths on the ALB DNS name returns successful service responses. | 4 Marks |

**Total Score: 20 Marks**

---

## Optional Enhancements

For advanced practice, you can attempt to implement:
- Configure HTTPS (SSL/TLS) traffic termination at the ALB.
- Set up an Auto Scaling Group (ASG) behind the ALB for elastic scaling.
- Configure customized static HTML error page responses (HTTP 502/504) on the ALB.
- Deploy the microservices using Docker containers.

---

## Real-World Use Case

This architecture forms the basis of modern containerized and VM-based microservices platforms. Deploying services across multiple availability zones prevents total platform outages from single datacenter disruptions. Path-based routing allows teams to use a single domain entry point to distribute traffic seamlessly to specialized backend service fleets, improving security, routing efficiency, and reducing public IP allocation costs.
