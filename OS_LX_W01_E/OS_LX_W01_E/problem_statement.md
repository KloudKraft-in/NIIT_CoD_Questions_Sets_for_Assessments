# Linux Lab: File Permissions, Ownership & Sudoers Security Configuration (Local VM)

Duration : 30 Min.

## Scenario

A security audit requires locking down directory and file access on a shared server. You must create a dedicated application group, set specific numeric permissions, ensure directory traversal restrictions, and configure least-privilege sudo privileges for a service user.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Create a user group

- Create a user group named appadmin and assign service account svc_deploy to it.

### 2. Create directory /var/deploy_repo with

- Create directory /var/deploy_repo with permissions 750 owned by svc_deploy:appadmin.

### 3. Configure files inside /var/deploy_repo

- Configure files inside /var/deploy_repo to default to 640 permissions.

### 4. Add a sudoers rule

- Add a sudoers rule in /etc/sudoers.d/svc_deploy granting permission to restart the nginx service without a password.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Group and user membership: appadmin group exists and svc_deploy is assigned | 3 Marks |
| **TC2** | Permission and ownership: /var/deploy_repo has 750 mode and correct ownership | 4 Marks |
| **TC3** | Sudoers rule: /etc/sudoers.d/svc_deploy contains valid syntax for NOPASSWD systemctl restart nginx | 3 Marks |

**Total Score: 10 Marks**
