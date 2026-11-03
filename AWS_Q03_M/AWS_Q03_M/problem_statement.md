# DevOps Lab: GitHub to Jenkins to Apache CI/CD

**Difficulty Level:** Medium

**Duration:** 90 Minutes

## Scenario

An organization wants to build a hands-on DevOps lab evaluation platform for students and professionals. Currently, manual evaluation of CI/CD assignments is time-consuming and difficult to scale. To solve this, the organization requires a fully automated pipeline that validates whether learners have correctly configured GitHub repositories, integrated Jenkins pipelines, configured webhooks, deployed applications to Apache, and executed successful CI/CD workflows. The system should also generate machine-readable logs/report files that can later be sent to a central backend server for automated scoring and assessment.

## Requirements

The learner must:

- Create a GitHub repository containing a web application.
- Configure Jenkins on an Ubuntu VM.
- Install and configure Apache Web Server.
- Configure GitHub webhooks to trigger Jenkins automatically on every code push.
- Create a Jenkins pipeline that:
  - Pulls code from GitHub
  - Deploys application files to Apache
  - Generates evaluation logs/report files
- Ensure that every successful commit automatically updates the live website.
- Generate a structured evaluation report file containing: pipeline status, deployment status, build information, and timestamp.

## Expected Workflow

```text
GitHub Push
      ↓
GitHub Webhook
      ↓
Jenkins Pipeline Trigger
      ↓
Code Clone
      ↓
Apache Deployment
      ↓
Evaluation Report Generation
      ↓
Website Updated
```

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
DEPLOYMENT=SUCCESS
PIPELINE_NAME=Code-Pipeline-Eval
BUILD_NUMBER=20
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 02:15:30 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                   | Description                      |
| ----------------------------- | -------------------------------- |
| **GitHub Repository**         | Source code repository           |
| **Jenkins Pipeline**          | Automated CI/CD workflow         |
| **Apache Deployment**         | Live deployed application        |
| **Webhook Integration**       | Automatic build trigger          |
| **Evaluation Report File**    | Structured deployment/build logs |
| **Successful Website Update** | Reflection of latest commits     |

## Technology Stack

| Technology          | Purpose                 |
| ------------------- | ----------------------- |
| **GitHub**          | Source Code Management  |
| **Jenkins**         | CI/CD Automation        |
| **Apache2**         | Web Hosting             |
| **Ubuntu**          | Server Environment      |
| **GitHub Webhooks** | Build Trigger Mechanism |
| **Shell Scripting** | Deployment Automation   |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases. The evaluation system checks the actual status of the integrations, builds, and Apache server deployments.

| Test Case | Requirement                            | Validation                                           | Marks   |
| --------- | -------------------------------------- | ---------------------------------------------------- | ------- |
| **TC1**   | **GitHub Webhook Configuration**       | Webhook configured correctly & Build auto-triggered  | 4 Marks |
| **TC2**   | **Jenkins Pipeline Job Creation**      | Job exists and configured correctly                  | 4 Marks |
| **TC3**   | **Jenkins Pipeline Execution Success** | Build completed successfully & Report file generated | 4 Marks |
| **TC4**   | **Apache Deployment Configuration**    | Application files deployed                           | 4 Marks |
| **TC5**   | **Live Website Updated Successfully**  | Website updated successfully with new content        | 4 Marks |

**Total Score: 20 Marks**

## Optional Enhancements

Learners may additionally implement:

- Maven build integration
- Docker-based deployment
- AWS CloudWatch logging
- JSON-based evaluation reports
- Automated backend API submission
- Multi-stage Jenkins pipelines

## Real-World Use Case

This solution simulates an industry-grade DevOps workflow used by organizations to automate deployments, validate CI/CD processes, monitor deployments, generate audit logs, and enable scalable hands-on lab evaluations. The generated logs/reports can later be integrated into centralized evaluation systems for automated grading and performance analysis.
