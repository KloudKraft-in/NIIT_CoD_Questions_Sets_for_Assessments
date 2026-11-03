# SAP Basis Lab: SAP GUI Session Management & Logon Group Routing Verification

Duration : 30 Min.

## Scenario
During peak morning logon, regional sales personnel experience erratic connection latencies and occasional session initialization drops. The Basis operations desk requires a verification of client SAP Logon Pad configurations against central Message Server routing rules. The administrator must validate SMLG logon groups, inspect response-time load distribution across dialog application servers, and enforce user concurrent session limits.

## Task Objectives
Perform the following SAP Basis diagnosis and document your findings:
1. Inspect SAP Logon Pad configuration parameters: verify Message Server hostname, System ID (SID), and group connection type.
2. Access transaction SMLG to inspect active logon groups, server response times, and connection distribution.
3. Audit user concurrent session governance: evaluate profile parameter rdisp/max_alt_modes and document the operational impact of unclosed user sessions on server memory buffers.

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
| **Rubric 1** | SAP Logon Pad configuration audit & message server SID validation | 4 Marks |
| **Rubric 2** | Logon group response-time load distribution check in SMLG | 3 Marks |
| **Rubric 3** | User session limits (rdisp/max_alt_modes) & hung desktop session triage | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is a **Manual Evaluation** assessment.
- Ensure thorough justification and alignment with SAP administration standards.
