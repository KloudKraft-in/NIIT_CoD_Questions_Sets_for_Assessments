# Java Lab: Log-to-Metric Error Pipeline

Duration : 60 Min.

## Scenario
Configure a log-to-metric processing rule pipeline `pipeline.json` to extract application metrics directly from raw server error signatures.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate or create `pipeline.json`.
2. Configure a JSON rule object with the following key-value criteria:
   - `pattern`: `"HTTP 500"`
   - `metric_name`: `"http_5xx_errors"`
   - `metric_type`: `"counter"`
3. Ensure the JSON structure is syntactically valid.

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | `pipeline.json` exists and is valid JSON | 3 Marks |
| **TC2   | `pattern` is set exactly to `"HTTP 500"` | 3 Marks |
| **TC3   | `metric_name` is `"http_5xx_errors"` and `metric_type` is `"counter"` | 4 Marks |

**Total Score: 10 Marks**
