# DevOps Lab: GitHub to Jenkins Automated Docker Image Build & AWS ECR Push Pipeline

**Difficulty Level:** Easy 
**Duration:** 30 Minutes

## Scenario

A cloud startup wants to automate the process of packaging their web application into a Docker container and storing it securely in AWS Elastic Container Registry (ECR). Currently, engineers build Docker images manually on their laptops, which is slow and prone to errors. To streamline deployments, the learner will set up a Jenkins pipeline that triggers automatically when code is pushed to GitHub, builds a Docker image from a provided `Dockerfile`, tags it cleanly, and pushes it to an existing AWS ECR repository.

## Requirements

The learner must:

- Fork or create a GitHub repository containing a simple web application (e.g., HTML/Node.js) and a valid `Dockerfile`.
- Access the provided Jenkins instance (with Docker installed and AWS credentials pre-configured).
- Configure a GitHub Webhook in your repository to send push events to your Jenkins server.
- Create a Jenkins Freestyle job or simple Pipeline (`Jenkinsfile`) that:
  - Clones the source code from your GitHub repository
  - Builds the Docker container image (`docker build -t niit-app .`)
  - Tags the image with `v1.0` or the Jenkins build number (`BUILD_NUMBER`)
  - Authenticates with AWS ECR (`aws ecr get-login-password`) and pushes the image (`docker push`)
- Verify that the Docker image successfully appears in your AWS ECR repository.
- Generate a simple evaluation report file recording the build and push status.

## Expected Workflow

```text
GitHub Push
      ↓
GitHub Webhook
      ↓
Jenkins Job Auto-Trigger
      ↓
Code Clone
      ↓
Docker Image Build (docker build)
      ↓
Image Tagging & ECR Login
      ↓
Docker Push to AWS ECR
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
DOCKER_BUILD=SUCCESS
IMAGE_TAG=v1.0
ECR_PUSH=SUCCESS
BUILD_NUMBER=10
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 11:30:15 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                | Description                |
| -------------------------- | -------------------------- |
| **GitHub Repository**      | Source code & Dockerfile   |
| **Jenkins Job / Pipeline** | Automated CI/CD build job  |
| **AWS ECR Repository**     | Target container registry  |
| **Webhook Integration**    | Automatic build trigger    |
| **Evaluation Report File** | Structured build/push logs |

## Technology Stack

| Technology  | Purpose                  |
| ----------- | ------------------------ |
| **GitHub**  | Source Code Management   |
| **Jenkins** | CI/CD Automation         |
| **Docker**  | Containerization         |
| **AWS ECR** | Container Image Registry |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case | Requirement                      | Validation                                               | Marks   |
| --------- | -------------------------------- | -------------------------------------------------------- | ------- |
| **TC1**   | **GitHub Webhook Configuration** | Webhook configured correctly & Job auto-triggered        | 2 Marks |
| **TC2**   | **Docker Image Build Check**     | Docker image built successfully without syntax errors    | 3 Marks |
| **TC3**   | **AWS ECR Authentication**       | Authenticated successfully with AWS ECR                  | 2 Marks |
| **TC4**   | **AWS ECR Image Push Check**     | Image successfully pushed & verified in AWS ECR registry | 3 Marks |

**Total Score: 10 Marks**
