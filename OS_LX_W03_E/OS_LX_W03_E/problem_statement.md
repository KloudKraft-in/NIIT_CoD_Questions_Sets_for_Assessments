# Linux Lab: Kernel Ring Buffer Diagnostics & Hardware Fault Triage via dmesg (Local VM)

Duration : 30 Min.

## Scenario

An enterprise web service crashed without writing an application stack trace. You must inspect the Linux kernel ring buffer using dmesg with human-readable timestamps to confirm whether the process was terminated by the Out-Of-Memory (OOM) killer or suffered a user-space segmentation fault.

## Task Objectives

Perform the following actions on your local Linux system:

### 1. Inspect Kernel Ring Buffer via dmesg

- Run `dmesg` with human-readable timestamps (`-T`) and filter for kernel events matching `oom-killer`, `Out of memory`, or `segfault`.
- Save the filtered kernel error log entries into `~/dmesg_errors.log`.

### 2. Extract Crashed Process Metrics

- Extract the terminated process name, process ID (PID), and total virtual memory pages at the time of termination from the kernel log.
- Save these metrics in JSON format inside `~/crash_diagnosis.json` using standard keys (such as `process_name`, `pid`, and `memory_pages`).

### 3. Classify Crash Origin Schema

- Classify the root cause of the crash as either `'KERNEL_OOM_KILL'` or `'USERSPACE_SEGFAULT'` under the `crash_origin` field in `~/crash_diagnosis.json`.
- Ensure `~/crash_diagnosis.json` is formatted as a valid JSON object.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Kernel ring buffer inspection: dmesg executed with human-readable timestamps (-T) | 3 Marks |
| **TC2** | Event extraction: correct PID, process name, and memory pages captured from dmesg log | 4 Marks |
| **TC3** | Classification schema: crash_diagnosis.json contains valid JSON with correct origin classification | 3 Marks |

**Total Score: 10 Marks**
