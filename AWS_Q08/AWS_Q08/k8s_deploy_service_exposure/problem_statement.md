# DevOps Lab: Kubernetes Pod Deployment & LoadBalancer Service Exposure

**Difficulty Level:** Easy to Medium  
**Duration:** 60 Minutes

## Scenario

A company wants to run its website on Kubernetes to ensure it stays online even if a container crashes. Currently, developers run single containers without orchestration, leading to downtime during maintenance or server failures. To establish a reliable container environment, the learner will write basic Kubernetes YAML manifests to deploy a 2-replica Nginx web server and expose it to external users using a `LoadBalancer` service.

## Requirements

The learner must:

- Access the provided Kubernetes cluster environment (e.g., Minikube / Kind / Cloud K8s).
- Create a simple Kubernetes Deployment manifest (`deployment.yaml`) that:
  - Deploys an Nginx web server (`nginx:latest`)
  - Configures exactly `2` replicas for basic high availability
  - Opens container port `80`
- Create a simple Kubernetes Service manifest (`service.yaml`) that:
  - Exposes the Nginx deployment
  - Configures the Service type as `LoadBalancer`
  - Maps incoming traffic on port `80` to target port `80`
- Apply both manifests using `kubectl apply -f` and verify that both pods are in the `Running` state.
- Generate a simple evaluation report file recording the deployment and service status.

## Expected Workflow

```text
Write Manifests (deployment.yaml, service.yaml)
      ↓
Apply Manifests (kubectl apply -f)
      ↓
Verify Pod Replicas (kubectl get pods)
      ↓
Verify Service (kubectl get svc)
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your environment should generate a report similar to the following:

```text
DEPLOYMENT_NAME=nginx-deployment
DESIRED_REPLICAS=2
AVAILABLE_REPLICAS=2
SERVICE_NAME=nginx-service
SERVICE_TYPE=LoadBalancer
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 12:15:30 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **Deployment Manifest**       | `deployment.yaml` with 2 replicas|
| **Service Manifest**          | `service.yaml` (LoadBalancer)    |
| **Running Pods**              | Verified active Kubernetes pods  |
| **Evaluation Report File**    | Structured cluster verification  |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **Kubernetes**      | Container Orchestration |
| **kubectl**         | Cluster CLI             |
| **YAML**            | Manifest Definition     |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **Deployment Creation Check**    | Deployment created successfully & active in cluster       | 10 Marks |
| **TC2** | **Pod Replica Verification**     | Exactly 2 replicas running healthy without crash loops    | 10 Marks |
| **TC3** | **Service LoadBalancer Check**   | Service created with LoadBalancer type exposing port 80   | 10 Marks |

**Total Score: 30 Marks**
