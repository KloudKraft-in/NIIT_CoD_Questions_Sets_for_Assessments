# DevOps Lab: GitHub to Jenkins Multi-Stage CI/CD Pipeline with Artifact Archiving

**Difficulty Level:** Medium  
**Duration:** 30 Minutes

## Scenario

A development team wants to establish a clear, structured Continuous Integration pipeline using Jenkins Declarative Pipeline syntax. Currently, developers run various build and lint scripts manually, making it difficult to track which version of the code produced a specific build artifact. To ensure traceability, the learner will create a `Jenkinsfile` in their GitHub repository containing three distinct stages: `Lint`, `Build`, and `Archive`. When code is pushed to GitHub, Jenkins will automatically trigger, execute the stages, simulate a build by generating a `build-artifact.txt` file, and use the Jenkins Artifact Archiver to save the output.

## Requirements

The learner must:

- Fork or create a GitHub repository containing sample project files.
- Access the provided Jenkins instance.
- Configure a GitHub Webhook in your repository to send push events to your Jenkins server.
- Create a `Jenkinsfile` in the root of your GitHub repository defining a Declarative Pipeline with three stages:
  - **Stage 1 (`Lint`)**: Executes a simple lint check (e.g., `echo "Running Lint Checks... Passed"`)
  - **Stage 2 (`Build`)**: Simulates a build process by creating an artifact file: `echo "Build completed successfully" > build-artifact.txt`
  - **Stage 3 (`Archive`)**: Uses the Jenkins `archiveArtifacts` directive to archive `build-artifact.txt`
- Create a Jenkins Pipeline job named `Multi-Stage-Pipeline` configured to pull `Jenkinsfile` from your GitHub repository.
- Verify that pushing code to GitHub automatically triggers the pipeline, executes all three stages successfully, and archives the artifact in the Jenkins job summary page.
- Generate a simple evaluation report file recording the pipeline stage execution and artifact archiving status.

## Expected Workflow

```text
GitHub Push
      ↓
GitHub Webhook
      ↓
Jenkins Pipeline Auto-Trigger (Multi-Stage-Pipeline)
      ↓
Stage 1: Lint (echo lint check)
      ↓
Stage 2: Build (create build-artifact.txt)
      ↓
Stage 3: Archive (archiveArtifacts 'build-artifact.txt')
      ↓
Verify Artifact in Jenkins Job Page
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
PIPELINE_NAME=Multi-Stage-Pipeline
STAGE_LINT=SUCCESS
STAGE_BUILD=SUCCESS
STAGE_ARCHIVE=SUCCESS
ARTIFACT_ARCHIVED=true
BUILD_NUMBER=4
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 11:45:20 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                | Description                     |
| -------------------------- | ------------------------------- |
| **GitHub Repository**      | Source code & `Jenkinsfile`     |
| **Jenkins Pipeline Job**   | Declarative CI/CD pipeline      |
| **Webhook Integration**    | Automatic build trigger         |
| **Archived Artifact**      | `build-artifact.txt` in Jenkins |
| **Evaluation Report File** | Structured pipeline stage logs  |

## Technology Stack

| Technology             | Purpose                |
| ---------------------- | ---------------------- |
| **GitHub**             | Source Code Management |
| **Jenkins**            | CI/CD Pipeline Engine  |
| **Declarative Groovy** | Pipeline Definition    |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case | Requirement                         | Validation                                            | Marks   |
| --------- | ----------------------------------- | ----------------------------------------------------- | ------- |
| **TC1**   | **GitHub Webhook Configuration**    | Webhook configured correctly                          | 4 Marks |
| **TC2**   | **Jenkins Pipeline Job Creation**   | Pipeline job created and configured                   | 4 Marks |
| **TC3**   | **Lint & Build Stage Execution**    | `Lint` & `Build` stages execute successfully          | 4 Marks |
| **TC4**   | **Artifact Creation Verification**  | `build-artifact.txt` successfully generated           | 4 Marks |
| **TC5**   | **Artifact Archiving Verification** | `build-artifact.txt` successfully archived in Jenkins | 4 Marks |

**Total Score: 20 Marks**
