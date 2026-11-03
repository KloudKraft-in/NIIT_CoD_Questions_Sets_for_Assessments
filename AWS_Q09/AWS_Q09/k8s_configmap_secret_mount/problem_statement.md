# DevOps Lab: Kubernetes Configuration Management with ConfigMaps & Secrets

**Difficulty Level:** Easy to Medium  
**Duration:** 60 Minutes

## Scenario

To keep application configurations neat and secure, a company wants to separate environment variables and sensitive passwords from container code. Hardcoding database credentials directly inside application images creates serious security vulnerabilities. To establish a secure practice, the learner will create a simple ConfigMap for application settings and a Kubernetes Secret for a database password, then deploy a single Pod that loads both configurations correctly.

## Requirements

The learner must:

- Access the provided Kubernetes cluster environment.
- Create a simple Kubernetes ConfigMap manifest (`configmap.yaml`) named `app-config` containing:
  - `APP_MODE`: `production`
- Create a simple Kubernetes Secret manifest (`secret.yaml`) named `db-secret` containing a base64-encoded password:
  - `password`: `c3VwZXJzZWNyZXQ=` (which decodes to `supersecret`)
- Create a Kubernetes Pod manifest (`pod.yaml`) named `config-demo-pod` that:
  - Runs a simple container (e.g., `busybox` or `nginx`)
  - Loads the `APP_MODE` value from the ConfigMap as an environment variable
  - Mounts the `db-secret` Secret as a volume at the path `/etc/secrets`
- Apply all manifests using `kubectl apply -f` and verify that the pod starts successfully.
- Generate a simple evaluation report file recording the ConfigMap, Secret, and Pod mount status.

## Expected Workflow

```text
Create ConfigMap & Secret Manifests
      ↓
Apply Manifests (kubectl apply -f)
      ↓
Create Pod Manifest with Env & Volume Mounts
      ↓
Apply Pod Manifest (kubectl apply -f)
      ↓
Verify Pod Running & Mounts Active
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your environment should generate a report similar to the following:

```text
CONFIGMAP_EXISTS=true
SECRET_EXISTS=true
POD_NAME=config-demo-pod
ENV_APP_MODE=production
SECRET_MOUNT_PATH=/etc/secrets
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 13:30:15 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **ConfigMap Manifest**        | `configmap.yaml` (`app-config`)  |
| **Secret Manifest**           | `secret.yaml` (`db-secret`)      |
| **Pod Manifest**              | `pod.yaml` with mounts configured|
| **Running Pod**               | Verified active Kubernetes pod   |
| **Evaluation Report File**    | Structured mount/config logs     |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **Kubernetes**      | Container Orchestration |
| **kubectl**         | Cluster CLI             |
| **YAML**            | Manifest Definition     |
| **Base64**          | Secret Encoding         |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **ConfigMap Creation Check**     | ConfigMap `app-config` exists with correct key/value      | 10 Marks |
| **TC2** | **Secret Creation Check**        | Secret `db-secret` exists with valid base64 password      | 10 Marks |
| **TC3** | **Pod Env & Volume Mount Check** | Pod running with ConfigMap env var & Secret volume mount  | 10 Marks |

**Total Score: 30 Marks**
