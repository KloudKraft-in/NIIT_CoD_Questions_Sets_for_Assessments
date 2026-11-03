# Log Analysis: Datadog & OpenSearch Log Aggregation Metrics

Duration : 90 Min.

## Scenario
Configure OpenSearch aggregation pipelines and Datadog Log Explorer queries to calculate percentile latencies (P95, P99) and monitor service SLA breaches.

## Target File Location & Creation
**File to Create/Update**: `student_workspace/solution.json`
**Input Resource File to Inspect**: `student_workspace/mysql_slow.log`

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Inspect `mysql_slow.log` in `student_workspace/`.
- Edit `solution.json` and record the required log analytics or findings.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Open and inspect `mysql_slow.log` inside `student_workspace/`.
3. Open `solution.json` in `student_workspace/` and perform the required modifications.
4. Save your changes (`Ctrl + S` or `Cmd + S`).
5. Open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress by running `python run.py` locally in the terminal.

## Validation
Once you have saved your files and verified your progress, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | solution.json exists and is valid JSON | 3 Marks |
| **TC2** | OpenSearch percentile aggregation syntax ('percentiles') correct | 3 Marks |
| **TC3** | P99 latency threshold value correctly calculated | 3 Marks |
| **TC4** | Datadog log search query syntax valid | 3 Marks |
| **TC5** | Service SLA breach status identified | 2 Marks |
| **TC6** | Group-by field ('service') included | 2 Marks |
| **TC7** | Time interval bucket set to 1m/5m | 2 Marks |
| **TC8** | Alert trigger condition specified | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- This is an auto-evaluated question. Ensure all code edits are properly saved and the 'run.py' checks pass before submission.
