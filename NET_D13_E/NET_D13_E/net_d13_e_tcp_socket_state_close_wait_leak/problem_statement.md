# Network Troubleshooting: TCP Socket State Distribution & Socket Leaks

Duration : 30 Min.

## Scenario

An API server running on Linux begins rejecting new client connections with 'Too many open files' and connection drops. An operations engineer ran `ss -tan` and captured a socket state summary alongside a thread dump excerpt. The network engineer must inspect the state distribution, differentiate between normal `TIME_WAIT` behavior and an application `CLOSE_WAIT` socket leak, and define the necessary code-level and OS-level fixes.

## Provided Artifacts & Input Files

The following diagnostic artifacts are pre-provisioned inside your `student_workspace/` directory for your inspection and analysis:

- `ss_tan_state_summary.txt`: Host TCP socket state distribution summary (`ss -tan`).
- `thread_dump_excerpt.txt`: Application thread dump excerpt capturing socket connection handling threads.
- `triage_report_template.md`: Starter template to record your technical analysis, findings, and remediation plan.

## Task Objectives

Perform the following network troubleshooting diagnosis and document your findings:

1. Create the setup script (`setup.sh`), make it executable (`chmod +x setup.sh`), and run it (`./setup.sh`) to set up the simulator environment.
2. Open and inspect `ss_tan_state_summary.txt` and `thread_dump_excerpt.txt` in `student_workspace/`.
3. Analyze the distribution of TCP socket states on the host and identify abnormal socket accumulations.
4. Explain the TCP connection termination state machine and differentiate between active and passive close states.
5. Determine the operational root cause behind the socket accumulation and explain how it leads to system resource exhaustion.
6. Specify both immediate operational mitigations and long-term application remediation in `student_workspace/triage_report.md`.

## Instructions to Perform the Task

1. Create the setup script `setup.sh` inside `student_workspace/`, grant execute permissions using `chmod +x setup.sh`, and run `./setup.sh`.
2. Review the scenario and inspect the pre-provisioned artifact files in your `student_workspace/`.
3. Formulate your technical diagnosis, packet/route analysis, and remediation plan based on the artifact evidence.
4. Save your comprehensive analysis inside `student_workspace/triage_report.md` (using `triage_report_template.md` as your guide).
5. Review your submission against the **Evaluation Rubric** below to ensure all technical criteria are addressed.
6. When complete, return to the platform dashboard and click **"Submit Final"**. This assessment is evaluated manually by the evaluation team.

## Validation

Once your deliverable is prepared and saved in the workspace, return to the platform dashboard and click the **"Submit Final"** button. This task is evaluated manually by the grading team.

## Evaluation Rubric:

| Item | Requirement / Criteria | Marks |
| :--- | :--- | :--- |
| **Rubric 1** | Quantitative analysis of host TCP socket states and identification of anomalous accumulation | 4 Marks |
| **Rubric 2** | Accurate technical distinction between TCP termination states and their lifecycle causes | 3 Marks |
| **Rubric 3** | Formulation of immediate operational mitigations and permanent application fixes | 3 Marks |

**Total Score: 10 Marks**

## Important Notes

- This is a **Manual Evaluation** assessment.
- Focus on sound networking principles, accurate protocol diagnosis, and structured remediation.
