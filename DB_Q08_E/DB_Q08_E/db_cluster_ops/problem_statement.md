# Databricks Lab : Cluster Operations & Terminations

Duration : 60 Min.

## Scenario

To optimize development costs, you are tasked with provisioning a single-node cluster with auto-termination configured to 20 minutes.

## Input Details

The environment has been pre-configured with the following resources:

- **Workspace:** Pre-configured through NIIT Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Cluster Name:** `<prefix>-ops-cluster` (e.g. `student-exam123-ops-cluster`)

## Task Objectives

### 1. Provision Cluster

- Name the cluster `<prefix>-ops-cluster`.
- Set auto-termination to 20 minutes.
- Enable Single Node mode and disable Photon Acceleration.
- Set node type to `Standard_D4s_v5`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                            | Marks   |
| ------------- | ------------------------------------------------------ | ------- |
| **TC1** | Cluster existence (`<prefix>-ops-cluster` exists)    | 4 Marks |
| **TC2** | Auto-termination setting (20 minutes)                  | 4 Marks |
| **TC3** | Single Node mode check (0 workers, singleNode profile) | 4 Marks |
| **TC4** | Node Type check (Standard_D4s_v5)                      | 4 Marks |
| **TC5** | Photon Acceleration Disabled                           | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
