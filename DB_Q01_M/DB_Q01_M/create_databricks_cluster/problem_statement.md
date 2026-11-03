# Databricks Lab : Single Node Cluster Setup

Duration : 60 Min.

## Scenario

As a Junior Cloud Engineer at NIIT, you are tasked with provisioning a development compute environment in Databricks. Your objective is to deploy a Databricks cluster configured as a single-node system with Photon acceleration disabled to save development costs.

## Input Details

The environment has been pre-configured with the following resources:

- **Workspace:** Pre-configured through NIIT Service credentials (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`)
- **Resource Group:** `rg-iRUN-LTM-Assessment`

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Cluster Name:** `<prefix>-db-cluster` (e.g. `student-exam123-db-cluster`)

## Task Objectives

Perform the following configuration steps directly in the Databricks Workspace Console or using the Databricks API:

### 1. Create Databricks Cluster

- **Cluster Name:** `<prefix>-db-cluster` (e.g. `student-exam123-db-cluster`)
- **Databricks Runtime Version:** Set the runtime to 17.3 LTS (`17.3.x-scala2.13`).
- **Node Type:** Set the node type to `Standard_D4s_v5`.
- **Single Node Cluster:** Enable Single Node mode (which sets worker count to 0 and uses the `singleNode` cluster profile).
- **Photon Acceleration:** Ensure Photon Acceleration is **Disabled**.
- **Autotermination:** Set the cluster to auto-terminate after 30 minutes of inactivity.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Databricks Workspace.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                 | Marks   |
| ------------- | ----------------------------------------------------------- | ------- |
| **TC1** | Cluster existence (`<prefix>-db-cluster` exists)          | 4 Marks |
| **TC2** | Spark Runtime Version (`17.3.x-scala2.13`)                | 4 Marks |
| **TC3** | Autotermination Verification (30 minutes)                   | 4 Marks |
| **TC4** | Single Node Mode Enabled (0 workers,`singleNode` profile) | 4 Marks |
| **TC5** | Node Type (`Standard_D4s_v5`) & Photon Disabled           | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The cluster name must follow Databricks naming rules.
