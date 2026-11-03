# GCP Lab: Google Cloud Platform (GCP) Virtual Machine Creation

Duration : 60 Min.

## Scenario

As a Junior Cloud Infrastructure Associate at Niit, you are tasked with setting up a lightweight, secure virtual machine on Google Cloud Platform (GCP) for a microservice deployment. You need to provision a Compute Engine instance with specific machine type and boot disk specifications.

## Input Details

The GCP environment is pre-configured with the following constraints:

- **Project ID:** (Your pre-allocated GCP project, e.g. `ltm-assessment-project`)
- **Zone:** `us-east4-a` (or as specified in your credentials sheet)
- **Boot Disk Type:** SSD Persistent Disk (`pd-ssd`)
- **Machine Type:** `n1-standard-1`

## Username & Naming Conventions

Your candidate prefix is the part of your GCP Console login email (provided in your credentials sheet) before the `@` symbol.
For example, if your GCP Console username is `akyghodake7769@gmail.com`, your prefix is **`akyghodake7769`**.

You must name your resources accordingly:

- **Compute Instance (VM) Name:** `vm-<prefix>` (e.g. `vm-akyghodake7769`)

## Task Objectives

Perform the following configurations using the Google Cloud Console or `gcloud` CLI:

### 1. Launch Compute Engine Instance

- **Instance Name:** `vm-<prefix>` (e.g., `vm-akyghodake7769`)
- **Region/Zone:** Deploy the instance in zone `us-east4-a` (or your pre-allocated zone).
- **Machine Type:** Select `n1-standard-1` under N1 machine family.
- **Operating System:** Deploy **Ubuntu Server 22.04 LTS** (or Ubuntu 20.04 LTS).
- **Boot Disk Size & Type:** Set size to exactly **10 GB** and type to **SSD Persistent Disk** (`pd-ssd`).
- **Instance State:** Ensure the instance is successfully deployed and in the **RUNNING** state.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Google Cloud environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                        | Marks   |
| ------------- | ------------------------------------------------------------------ | ------- |
| **TC1** | Google Cloud Platform project access check                         | 0 Marks |
| **TC2** | Virtual Machine existence (`vm-<prefix>` in zone `us-east4-a`) | 4 Marks |
| **TC3** | Machine type validation (must be`n1-standard-1`)                 | 4 Marks |
| **TC4** | OS Image validation (must be Ubuntu-based)                         | 4 Marks |
| **TC5** | Boot disk size & type validation (10 GB size,`pd-ssd` type)      | 4 Marks |
| **TC6** | Instance running status (must be`RUNNING`)                       | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The VM must be actively running during evaluation.
- Do not create extra resources outside the requirements.
