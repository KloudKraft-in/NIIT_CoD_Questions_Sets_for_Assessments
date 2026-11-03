# Storage Lab: Storage Queue Depth & Disk Utilization Metric Anomaly Detection

Duration : 30 Min.

## Scenario
A web application is intermittently timing out. The server monitoring dashboard shows CPU at 25% and Memory at 40%, but disk response time is degraded. The engineer must inspect `iostat_capture.log` (captured via `iostat -xz 1 10`), parse %util (disk saturation), average queue size (avgqu-sz), and write await times, determine whether the storage device is experiencing I/O queuing, and document a structured anomaly analysis in `iostat_analysis.json`.

## Task Objectives

Perform the following storage latency and queue depth analysis tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`iostat_capture.log`**: Real-time disk I/O metrics captured via `iostat -xz`.
> - **`iostat_analysis.json`**: Starter diagnostic analysis JSON with `TODO_*` placeholders.

1. Inspect `iostat_capture.log` to parse device utilization, average queue depth, and latency breakdowns.
2. Evaluate whether device utilization indicates storage controller saturation (e.g. `sda` > 90% utilization).
3. Differentiate between read and write latency components to isolate the primary I/O bottleneck (`w_await` vs `r_await`).
4. Record your diagnostic metrics and saturation verdict in `iostat_analysis.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Review the pre-staged `iostat_capture.log` to analyze queue depths, awaiting times, and disk utilization.
3. Update `iostat_analysis.json` inside the `student_workspace/` directory, replacing all `TODO_*` placeholders with your verified metrics.
4. Verify your storage configurations locally by executing:
   ```bash
   python run.py
   ```
5. Once verified, return to the platform dashboard and click **"Run Tests"** / **"Full Eval"** to evaluate your score!

## Validation
Once your storage tasks are executed, return to the platform dashboard and click the **"Run Tests"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Command execution: iostat -xz correctly invoked with appropriate sampling interval and count | 2 Marks |
| **TC2** | Utilization parsing: %util extracted accurately and compared against saturation baseline | 2 Marks |
| **TC3** | Queue depth evaluation: avgqu-sz correctly interpreted indicating queued I/O requests | 2 Marks |
| **TC4** | Latency breakdown: r_await and w_await correctly extracted to isolate write-heavy bottleneck | 2 Marks |
| **TC5** | Summary report: iostat_analysis.json contains structured metrics and clear bottleneck conclusion | 2 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
