# DevOps Lab: Automating Web Server Setup via EC2 User Data

**Difficulty Level:** Easy  
**Duration:** 30 Minutes

## Scenario

You are a DevOps engineer responsible for automating web server provisioning. When a new EC2 instance is created, Nginx must be installed automatically, the service must start, and the team should be able to access it via HTTP without manual SSH access.

## Task Objectives

Perform the following actions in the environment:

### 1. Configure EC2 User Data
### 2. Launch EC2 Instance
### 3. Verify Nginx Installation

## Requirements

- **EC2 Instance Name:** `nginx-server-<your-labskraft-username>`
- Configure **User Data** to install and start Nginx.
- Ensure the instance has a Public IP.
- Ensure Security Group allows incoming HTTP traffic on Port 80.

## Expected Workflow

Follow the task objectives sequentially to implement the architecture.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                            | Marks   |
| --------- | -------------------------------------- | ------- |
| **TC1**   | EC2 Instance Existence and Running     | 2 Marks |
| **TC2**   | Security Group allows HTTP Port 80     | 1 Marks |
| **TC3**   | Security Group allows SSH Port 22      | 2 Marks |
| **TC4**   | EC2 Instance has a Public IP assigned  | 2 Marks |
| **TC5**   | EC2 User Data script is present        | 1 Marks |
| **TC6**   | Nginx accessible via HTTP on Public IP | 2 Marks |

**Total Score: 10 Marks**

## Real-World Use Case

This solution simulates industry-grade workflows used by organizations to automate infrastructure deployments, validate configurations, and enable scalable hands-on lab evaluations.
