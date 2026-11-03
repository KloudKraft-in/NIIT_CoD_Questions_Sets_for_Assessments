# SAP Basis Lab: Financial Close Batch Abort — SM37 Job Log & ST22 Memory Dump Forensic Remediation

Duration : 60 Min.

## Scenario
During month-end financial close, the core revenue accrual batch job FI_POST_ACCRUAL aborts with status CANCELED after running for 3 hours. The job log references an internal ABAP runtime error. The Basis engineer must pull the job log in SM37, isolate the exact termination timestamp, cross-reference transaction ST22 to analyze the memory short dump, check for partial database postings, and execute the restart SOP safely.

## Task Objectives
Perform the following SAP Basis diagnosis and document your findings:
1. Access SM37, extract the job log for FI_POST_ACCRUAL, and record the exact cancellation message and timestamp.
2. Navigate to ST22, locate the matching ABAP short dump (TSV_TNEW_PAGE_ALLOC_FAILED), and analyze roll/extended/heap memory allocations.
3. Execute database commit and idempotency verification to determine whether partial document numbers were posted.
4. Apply batch restart SOP: split processing variant into smaller fiscal period blocks and initiate safe restart.

## Instructions to Perform the Task
1. Review the SAP NetWeaver system logs, transaction codes, and landscape context detailed above.
2. Formulate your technical diagnosis, instance triage, or corrective action procedure.
3. Save all required documentation or deliverable notes inside the `student_workspace` directory.
4. Review your submission against the **Evaluation Rubric** below to ensure all criteria are covered.
5. When complete, return to the platform dashboard and click **"Submit Final"**. This assessment is evaluated manually by the evaluation team.

## Validation
Once your diagnosis report is ready and saved, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:
| Item | Requirement / Criteria | Marks |
| :--- | :--- | :--- |
| **Rubric 1** | Correlation of canceled financial batch job in SM37 with ST22 dump | 5 Marks |
| **Rubric 2** | Forensic analysis of TSV_TNEW_PAGE_ALLOC_FAILED roll/extended/heap memory quotas | 5 Marks |
| **Rubric 3** | Idempotency validation verifying partial database commit state | 5 Marks |
| **Rubric 4** | Authoring compliant batch rerun change request with reduced packet size parameters | 5 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is a **Manual Evaluation** assessment.
- Ensure thorough justification and alignment with SAP administration standards.
