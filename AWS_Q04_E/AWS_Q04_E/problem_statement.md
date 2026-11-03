# DevOps Lab: GitHub Webhook Trigger & Jenkins Parameterized Backup Job

**Difficulty Level:** Easy  
**Duration:** 30 Minutes

## Scenario

A system administrator wants to automate the process of creating archive backups of project files whenever code changes are pushed to GitHub. Instead of manually logging into the server to copy files and manage backup folders, the learner will configure a Jenkins job triggered automatically by a GitHub webhook. The job will accept a parameter (e.g., `BACKUP_ENV`), clone the repository, and create a compressed archive (`backup.tar.gz`) of the workspace.

## Requirements

The learner must:

- Fork or create a GitHub repository containing sample project files (e.g., `README.md`, `index.html`, `app.js`).
- Access the provided Jenkins instance.
- Configure a GitHub Webhook in your repository to send push events to your Jenkins server.
- Create a Parameterized Jenkins Freestyle job or simple Pipeline named `Project-Backup-Job` that:
  - Defines a String Parameter named `BACKUP_ENV` with a default value of `staging`
  - Clones the source code from your GitHub repository
  - Executes a shell build step: `tar -czvf backup_${BACKUP_ENV}.tar.gz .`
- Ensure that pushing code to GitHub automatically triggers the job and successfully creates the backup archive in the Jenkins workspace.
- Generate a simple evaluation report file recording the job execution and archive verification.

## Expected Workflow

```text
GitHub Push
      ↓
GitHub Webhook
      ↓
Jenkins Job Auto-Trigger (with default BACKUP_ENV)
      ↓
Code Clone
      ↓
Shell Execution (tar -czvf backup_staging.tar.gz .)
      ↓
Verify Archive Created in Workspace
      ↓
Evaluation Report Generation
```

## Sample Evaluation Report

Your pipeline should generate a report similar to the following:

```text
GIT_CLONE=SUCCESS
JOB_NAME=Project-Backup-Job
PARAMETER_BACKUP_ENV=staging
ARCHIVE_CREATED=true
BUILD_NUMBER=3
FINAL_STATUS=SUCCESS
TIMESTAMP=Thu May 15 10:30:15 UTC 2026
```

## Deliverables

The final solution should include:

| Deliverable                   | Description                   |
| ----------------------------- | ----------------------------- |
| **GitHub Repository**         | Source code repository        |
| **Jenkins Parameterized Job** | Automated backup job          |
| **Webhook Integration**       | Automatic build trigger       |
| **Evaluation Report File**    | Structured job execution logs |

## Technology Stack

| Technology      | Purpose                |
| --------------- | ---------------------- |
| **GitHub**      | Source Code Management |
| **Jenkins**     | CI/CD Automation       |
| **Linux Shell** | Archive Automation     |

## Verification & Grading Criteria

Your performance will be automatically evaluated based on the following test cases.

| Test Case | Requirement                      | Validation                                                | Marks   |
| --------- | -------------------------------- | --------------------------------------------------------- | ------- |
| **TC1**   | **GitHub Webhook Configuration** | Webhook configured correctly & Job auto-triggered         | 2 Marks |
| **TC2**   | **Parameterized Job Config**     | Job exists with `BACKUP_ENV` parameter configured         | 3 Marks |
| **TC3**   | **Backup Job Execution Success** | Job executed successfully and generated report            | 2 Marks |
| **TC4**   | **Backup Archive Verification**  | `backup_staging.tar.gz` successfully created in workspace | 3 Marks |

**Total Score: 10 Marks**
