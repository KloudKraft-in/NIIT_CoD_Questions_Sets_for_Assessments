# GCP Lab: Google Cloud Storage (GCS) Bucket & Versioning Setup

Duration : 60 Min.

## Scenario

As a Junior Cloud Engineer at LabsKraft, you are tasked with setting up a highly available object storage environment in Google Cloud Platform (GCP). You need to provision a GCS Bucket, configure it in standard storage class, ensure it is deployed in a specific region, enable object versioning for data safety, and upload a test file to verify connectivity.

## Input Details

The GCP environment is pre-configured with the following constraints:

- **Project ID:** (Your pre-allocated GCP project, e.g. `ltm-assessment-project`)
- **Region:** `us-east4` (Northern Virginia region)
- **Default Storage Class:** Standard (`STANDARD`)
- **Test File to Upload:** Create a local text file named `welcome.txt` containing any text content (e.g. `Welcome to LabsKraft GCP Assessment!`).

## Username & Naming Conventions

Your candidate prefix is the part of your GCP Console login email (provided in your credentials sheet) before the `@` symbol.
For example, if your GCP Console username is `akyghodake7769@gmail.com`, your prefix is **`akyghodake7769`**.

You must name your resources accordingly:

- **Storage Bucket Name:** `bkt-<prefix>` (Bucket names must be globally unique. E.g. `bkt-akyghodake7769`)

## Task Objectives

Perform the following configurations using the Google Cloud Console or `gsutil` CLI:

### 1. Create Google Cloud Storage Bucket

- **Bucket Name:** `bkt-<prefix>` (e.g., `bkt-akyghodake7769`)
- **Location Type:** Select **Region** and set location to `us-east4`.
- **Default Storage Class:** Standard (`STANDARD`).
- **Object Versioning:** Enable Object Versioning explicitly on the bucket to preserve old versions of files.
- **Upload File:** Upload your created text file `welcome.txt` into the root of this bucket.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Google Cloud environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                    | Marks   |
| ------------- | ------------------------------------------------------------------------------ | ------- |
| **TC1** | Google Cloud Storage service access check                                      | 0 Marks |
| **TC2** | Bucket existence (`bkt-<prefix>` created)                                    | 4 Marks |
| **TC3** | Location validation (must be in region`us-east4`)                            | 4 Marks |
| **TC4** | Object existence (`welcome.txt` file is successfully uploaded to the bucket) | 4 Marks |
| **TC5** | Object Versioning check (must be explicitly enabled on the bucket)             | 4 Marks |
| **TC6** | Storage Class check (Standard Storage Class)                                   | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Bucket names must be lowercase alphanumeric and dashes only.
