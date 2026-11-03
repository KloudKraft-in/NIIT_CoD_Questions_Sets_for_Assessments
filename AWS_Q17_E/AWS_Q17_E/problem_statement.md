# DevOps Lab: Kubernetes Persistent Volumes with AWS EBS

**Difficulty Level:** Easy  
**Duration:** 30 Minutes

## Scenario

Your team is running a stateful application in Kubernetes that stores user-generated files. Currently, data is lost whenever pods restart. To fix this, you decide to use AWS EBS as persistent storage dynamically provisioned and mounted to a Kubernetes Deployment.

## Task Objectives

Perform the following actions in the environment:

### 1. Dynamically Provision EBS Volume
### 2. Create PersistentVolumeClaim
### 3. Deploy Application with Volume Mount

## Requirements

- **PersistentVolumeClaim Name:** `data-pvc`
- **Access Mode:** ReadWriteOnce
- **Storage:** 2Gi
- **Deployment Name:** `nginx-app`
- Mount the PVC to the deployment at path `/usr/share/nginx/html`.

## Expected Workflow

Follow the task objectives sequentially to implement the architecture.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                               | Marks   |
| --------- | ----------------------------------------- | ------- |
| **TC1**   | StorageClass exists for EBS provisioner   | 2 Marks |
| **TC2**   | PersistentVolumeClaim exists              | 1 Marks |
| **TC3**   | PersistentVolumeClaim is Bound            | 2 Marks |
| **TC4**   | Deployment exists and Running             | 2 Marks |
| **TC5**   | Deployment requests exact storage size    | 1 Marks |
| **TC6**   | Volume is mounted in Pods at correct path | 2 Marks |

**Total Score: 10 Marks**

## Real-World Use Case

This solution simulates industry-grade workflows used by organizations to automate infrastructure deployments, validate configurations, and enable scalable hands-on lab evaluations.
