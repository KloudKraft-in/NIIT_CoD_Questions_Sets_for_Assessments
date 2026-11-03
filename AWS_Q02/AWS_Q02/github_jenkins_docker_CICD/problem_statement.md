# DevOps Lab: GitHub to Jenkins to Docker CI/CD

**Duration:** 75 Minutes

## Scenario

An organization wants to create a scalable DevOps hands-on lab platform where learners are evaluated based on real CI/CD pipeline execution instead of manual assessment. Your objective is to design and implement an automated CI/CD pipeline using GitHub, Jenkins, and Docker to automatically build, containerize, and deploy an application whenever code is pushed to a GitHub repository.

## Requirements

The learner must:

- Create a GitHub repository containing a web application.
- Configure Jenkins on an Ubuntu VM.
- Install and configure Docker.
- Configure GitHub webhooks to trigger Jenkins automatically on every push event.
- Create a Jenkins pipeline that:
  - Clones code from GitHub
  - Builds a Docker image
  - Runs a Docker container
  - Deploys the application
  - Generates evaluation logs/report files
- Ensure that every successful commit automatically updates the running Docker application.
- Generate a structured evaluation report file containing: build status, Docker image creation status, container deployment status, pipeline information, and timestamp.

## Expected Workflow

```text
GitHub Push
      ↓
GitHub Webhook
      ↓
Jenkins Pipeline Trigger
      ↓
Clone Repository
      ↓
Docker Image Build
      ↓
Docker Container Deployment
      ↓
Evaluation Report Generation
      ↓
Application Updated
```

## Expected Docker Operations

The pipeline should automate the following operations:

- `docker build`
- `docker run`
- `docker ps`
- `docker stop`
- `docker rm`

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
DOCKER_BUILD=SUCCESS
DOCKER_CONTAINER_DEPLOYMENT=SUCCESS
PIPELINE_NAME=Docker-Pipeline-Eval
BUILD_NUMBER=12
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 03:10:00 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                        | Description                      |
| ---------------------------------- | -------------------------------- |
| **GitHub Repository**        | Application source code          |
| **Jenkins Pipeline**         | Automated CI/CD workflow         |
| **Dockerfile**               | Container build instructions     |
| **Running Docker Container** | Live deployed application        |
| **Webhook Integration**      | Automatic pipeline trigger       |
| **Evaluation Report File**   | Structured deployment/build logs |

## Technology Stack

| Technology                | Purpose                |
| ------------------------- | ---------------------- |
| **GitHub**          | Source Code Management |
| **Jenkins**         | CI/CD Automation       |
| **Docker**          | Containerization       |
| **Ubuntu**          | Server Environment     |
| **GitHub Webhooks** | Build Trigger          |
| **Shell Scripting** | Deployment Automation  |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases. The evaluation system checks the actual status of the integrations, builds, and containers.

| Test Case     | Requirement                            | Validation                                            | Marks    |
| ------------- | -------------------------------------- | ----------------------------------------------------- | -------- |
| **TC1** | **GitHub Integration & Trigger** | Webhook configured correctly & Build auto-triggered   | 10 Marks |
| **TC2** | **Jenkins Pipeline Execution**   | Build completed successfully & Report file generated  | 10 Marks |
| **TC3** | **Docker Build & Deployment**    | Docker image created & Container running successfully | 10 Marks |

**Total Score: 30 Marks**

## Optional Enhancements

Learners may additionally implement:

- Docker Compose
- Nginx reverse proxy
- Multi-container deployments
- DockerHub integration
- AWS ECR integration
- Kubernetes deployment
- AWS CloudWatch logging
- JSON-based evaluation reports
- Backend API integration

## Real-World Use Case

This solution simulates real-world DevOps workflows used in modern organizations for automated containerized deployments, CI/CD automation, scalable application delivery, deployment monitoring, log-based validation, and hands-on DevOps assessment platforms. The generated evaluation logs/reports can later be integrated into centralized scoring systems for automated grading and performance analysis.
