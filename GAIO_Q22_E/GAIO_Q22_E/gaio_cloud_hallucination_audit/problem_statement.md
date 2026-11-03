# GenAI Ops: Imaginary Cloud Resource & Fake API Hallucination Audit

Duration : 45 Min.

## Scenario
An AI assistant generated Terraform code and AWS Boto3 scripts containing non-existent resource types (`aws_s3_super_bucket`) and fake methods (`boto3.delete_everything()`). Audit the code.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/cloud_audit.json`
**Input Resource File to Inspect**: `student_workspace/ai_generated_infra.tf`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `ai_generated_infra.tf` in `student_workspace/`.
- Create or update `student_workspace/cloud_audit.json` and populate it with valid analysis results.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `ai_generated_infra.tf` inside `student_workspace/`.
3. Create or open `student_workspace/cloud_audit.json` in `student_workspace/` and record your answers.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | cloud_audit.json exists | 3 Marks |
| **TC2** | Fake Terraform resource 'aws_s3_super_bucket' flagged | 3 Marks |
| **TC3** | Fake Boto3 method 'delete_everything()' flagged | 2 Marks |
| **TC4** | Valid AWS resources ('aws_s3_bucket') preserved as legitimate | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
