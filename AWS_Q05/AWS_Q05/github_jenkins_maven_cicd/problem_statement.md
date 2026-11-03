# DevOps Lab: GitHub to Jenkins Automated Maven CI/CD Pipeline

**Difficulty Level:** Easy to Medium  
**Duration:** 60 Minutes

## Scenario

A software development team wants to introduce automated building and packaging for their Java applications. Currently, developers compile code on their local laptops, which leads to "it works on my machine" inconsistencies and accidental syntax errors reaching the main codebase. To establish a smooth and reliable workflow, the team requires an automated CI/CD pipeline. The learner will configure a Jenkins pipeline triggered by a GitHub webhook. The pipeline will pull a simple Java project, compile it using Maven, and package it into a deployable artifact (.jar/.war).

## Requirements

The learner must:

- Fork or create a GitHub repository containing a simple Maven-based Java application (with a `pom.xml`).
- Access the provided Jenkins instance (with Maven plugins pre-installed).
- Configure a GitHub Webhook in your repository to send push events to your Jenkins server.
- Create a Jenkins Freestyle job or simple Pipeline (`Jenkinsfile`) that:
  - Clones the source code from your GitHub repository
  - Executes a Maven clean package (`mvn clean package` or `mvn clean compile`)
- Ensure the build completes successfully and the compiled Maven artifact is generated in the `target` directory.
- Generate a simple evaluation report file recording the build status.

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
Maven Build (mvn clean package)
      ↓
Artifact Verification (.jar/.war)
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
MAVEN_BUILD=SUCCESS
ARTIFACT_GENERATION=SUCCESS
BUILD_NUMBER=5
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 10:15:30 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                         | Description                      |
| ----------------------------------- | -------------------------------- |
| **GitHub Repository**         | Source code repository           |
| **Jenkins Job / Pipeline**    | Automated CI/CD build job        |
| **Webhook Integration**       | Automatic build trigger          |
| **Evaluation Report File**    | Structured build logs            |

## Technology Stack

| Technology                | Purpose                 |
| ------------------------- | ----------------------- |
| **GitHub**          | Source Code Management  |
| **Jenkins**         | CI/CD Automation        |
| **Maven**           | Build & Dependency Tool |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case     | Requirement                            | Validation                                                | Marks    |
| ------------- | -------------------------------------- | --------------------------------------------------------- | -------- |
| **TC1** | **GitHub Webhook Configuration** | Webhook configured correctly & Job auto-triggered         | 10 Marks |
| **TC2** | **Maven Build Execution**        | Maven `clean compile` / `clean package` completed         | 10 Marks |
| **TC3** | **Maven Artifact Verification**  | Compiled artifact (.jar/.war) successfully generated      | 10 Marks |

**Total Score: 30 Marks**
