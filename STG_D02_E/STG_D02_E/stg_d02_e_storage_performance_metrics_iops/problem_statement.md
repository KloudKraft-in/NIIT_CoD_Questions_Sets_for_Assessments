# Storage Lab: Storage Performance Metrics — IOPS, Throughput & Latency Dissection

Duration : 30 Min.

## Scenario
An enterprise monitoring alert reports that an analytics batch job is taking 8 hours instead of 2 hours, despite disk capacity being at only 40%. The engineer is provided with I/O benchmark logs containing read/write operation counts, block sizes (4 KB vs 256 KB), transfer rates (MB/s), and response times (ms). The engineer must parse the metrics to explain why a workload can be bottlenecked on IOPS even when throughput is far below disk limits, and output a performance analysis summary.

## Task Objectives

Perform the following storage performance analysis tasks inside your `student_workspace` directory:

> **Pre-Staged Files in `student_workspace/`:**
> - **`fio_summary.log`**: Raw benchmark output containing 4KB random read and 256KB sequential read profiles.
> - **`perf_diagnosis.json`**: Starter diagnosis report with `TODO_*` placeholders.

1. Inspect the raw benchmark output in `fio_summary.log` and extract the IOPS, block sizes, throughput rates, and latency figures for each profile.
2. Calculate the achieved throughput from the IOPS and block size metrics using standard storage formulas.
3. Determine whether the storage subsystem is IOPS-bound, throughput-bound, or latency-bound, providing concise technical justification.
4. Document your calculations, identified bottleneck, and diagnosis in `perf_diagnosis.json`.

## Instructions to Perform the Task
1. Open your assessment **Terminal** or storage management CLI interface.
2. Execute the required storage management commands, volume operations, or configuration edits.
3. If configuration files, backup manifests, or diagnostic reports are required, save them inside the `student_workspace` directory.
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
| **TC1** | Log inspection: successfully parse IOPS, average completion latency, and transfer rates from fio_summary.log | 4 Marks |
| **TC2** | Metric calculation: accurate computation of theoretical vs measured throughput across different block size profiles | 3 Marks |
| **TC3** | Bottleneck diagnosis: perf_diagnosis.json correctly identifies IOPS throttling due to small 4KB random reads | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** storage assessment.
- Ensure all created volumes, files, and scripts are properly configured and saved before submitting.
