# DevOps Lab: GitHub Actions to Amazon ECR CI/CD


**Difficulty Level:** Easy  
**Duration:** 30 Minutes

## Scenario

Your organization wants to standardize container deployments using GitHub Actions. Every time code is pushed to the main branch, a Docker image should be built, tagged, and pushed securely to Amazon ECR.

## Task Objectives

Perform the following actions in the environment:

### 1. Create AWS ECR Repository
### 2. Configure GitHub Secrets
### 3. Create GitHub Actions Workflow

## Requirements

- **ECR Repository Name:** `webapp-repo-<your-labskraft-username>`
- Authenticate securely with AWS inside GitHub Actions.
- Build the Docker image from a standard Dockerfile.
- Push the Docker image to the ECR repository.

## Expected Workflow

Follow the task objectives sequentially to implement the architecture.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement                                           | Marks   |
| --------- | ----------------------------------------------------- | ------- |
| **TC1**   | ECR Repository Existence                              | 2 Marks |
| **TC2**   | ECR Repository configured with Mutability constraints | 1 Marks |
| **TC3**   | ECR Repository contains at least one Image            | 2 Marks |
| **TC4**   | Image is correctly tagged                             | 2 Marks |
| **TC5**   | ECR Image Vulnerability Scanning is configured        | 1 Marks |
| **TC6**   | Docker Image architecture is standard                 | 2 Marks |

**Total Score: 10 Marks**

## Real-World Use Case

This solution simulates industry-grade workflows used by organizations to automate infrastructure deployments, validate configurations, and enable scalable hands-on lab evaluations.
