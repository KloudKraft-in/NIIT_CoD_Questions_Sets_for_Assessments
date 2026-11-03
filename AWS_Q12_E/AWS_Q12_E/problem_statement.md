# DevOps Lab: AWS CodePipeline Automated S3 Static Website CI/CD

**Difficulty Level:** Easy

**Duration:** 30 Minutes

## Scenario

A cloud development team wants a fully managed, serverless CI/CD pipeline for their frontend web application. Currently, developers manually upload HTML/CSS files to an S3 bucket, which is error-prone and lacks version control tracking. To establish a modern GitOps workflow, the team requires an automated AWS CodePipeline. The learner will create an AWS CodeCommit repository (or connect a GitHub repo), configure an S3 bucket for static website hosting, and build an AWS CodePipeline that automatically deploys new commits directly to the S3 bucket.

## Requirements

The learner must:

- Create an AWS CodeCommit repository (or connect a GitHub repository) containing a static web application (e.g., `index.html`).
- Create an AWS S3 Bucket named `labskraft-web-app-<your-labskraft-username>` configured for **Static Website Hosting**.
- Configure appropriate bucket policies or public access settings to allow public read access to the web objects.
- Build an AWS CodePipeline named `labskraft-frontend-pipeline-<your-labskraft-username>` that:
  - Uses the CodeCommit/GitHub repository as the **Source** stage.
  - Uses the destination S3 Bucket as the **Deploy** stage (using AWS CodeDeploy / S3 deploy provider).
- Ensure the pipeline executes successfully upon a git push, and the web application is accessible via the S3 static website endpoint.

## Expected Workflow

```text
Git Push (CodeCommit/GitHub)
      ↓
AWS CodePipeline Auto-Trigger
      ↓
Source Stage (Artifact Checkout)
      ↓
Deploy Stage (S3 Static Website)
      ↓
Public Endpoint Verification
```

## Sample Evaluation Report

Your pipeline should generate a state verification log similar to the following:

```text
REPO_CONFIGURED=SUCCESS
S3_HOSTING_ENABLED=SUCCESS
PIPELINE_STATUS=SUCCESS
DEPLOYED_FILE=index.html
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 10:15:30 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable           | Description                    |
| --------------------- | ------------------------------ |
| **Source Repository** | CodeCommit / GitHub repository |
| **S3 Hosting Bucket** | Static website destination     |
| **AWS CodePipeline**  | Automated CI/CD pipeline       |

## Technology Stack

| Technology           | Purpose                |
| -------------------- | ---------------------- |
| **AWS CodeCommit**   | Source Code Management |
| **AWS CodePipeline** | CI/CD Orchestration    |
| **AWS S3**           | Static Website Hosting |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case | Requirement                         | Validation                                               | Marks   |
| --------- | ----------------------------------- | -------------------------------------------------------- | ------- |
| **TC1**   | **Repository Setup**                | Repo exists                                              | 2 Marks |
| **TC2**   | **S3 Hosting Setup**                | S3 bucket configured for static hosting                  | 3 Marks |
| **TC3**   | **AWS CodePipeline Configuration**  | CodePipeline exists connecting Source to S3 Deploy stage | 2 Marks |
| **TC4**   | **Pipeline Execution & Deployment** | Pipeline execution succeeded & index.html exists in S3   | 3 Marks |

**Total Score: 10 Marks**
