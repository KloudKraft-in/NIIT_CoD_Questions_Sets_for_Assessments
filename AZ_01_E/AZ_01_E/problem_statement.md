# Azure Lab: Azure Storage Account & Container Setup

Duration : 60 Min.

## Scenario

As a Junior Cloud Engineer at LabsKraft, you are tasked with provisioning a secure object storage environment in Microsoft Azure. Your objective is to deploy a Storage Account with standard local redundancy and a private blob container to securely store application assets.

## Input Details

The environment has been pre-configured with the following resources:

- **Subscription:** LabsKraft
- **Resource Group:** `rg-iRUN-LTM-Assessment`
- **Region:** Asia Pacific East Asia (use `eastasia` region)
- **Preferred Storage Type:** Standard LRS (`Standard_LRS`)

## Username & Naming Conventions

Your candidate prefix is the part of your Azure login email before the `@` symbol.
For example, if your Azure username is `ltmdemo01@michaelkloudkrafthotmail.onmicrosoft.com`, your prefix is **`ltmdemo01`**.

You must name your resources accordingly:

- **Storage Account Name:** `store<prefix>` (e.g. `storeltmdemo01`)

## Task Objectives

Perform the following configuration steps directly in the Azure Portal or using the Azure CLI:

### 1. Create Storage Account

- **Storage Account Name:** `store<prefix>` (Storage Account names must be between 3 and 24 characters, using numbers and lowercase letters only with no special characters. E.g. `storeltmdemo01`)
- **Resource Group:** Place the Storage Account in the pre-existing Resource Group `rg-iRUN-LTM-Assessment`.
- **Location:** Deploy the Storage Account in the `eastasia` region.
- **Storage Sku:** Standard LRS (`Standard_LRS`)
- **Security:** Ensure that secure transfer (HTTPS-only traffic) is explicitly enabled/enforced for the storage account.
- **Blob Container:** Create a private container named `assets` inside the storage account.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Azure cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                     | Marks   |
| ------------- | ------------------------------------------------------------------------------- | ------- |
| **TC1** | Resource Group validation (`rg-iRUN-LTM-Assessment` exists and is accessible) | 0 Marks |
| **TC2** | Storage Account existence (`store<prefix>` in `eastasia`)                   | 4 Marks |
| **TC3** | Storage Account SKU verification (Standard LRS)                                 | 4 Marks |
| **TC4** | Blob Container existence (container named`assets` exists)                     | 4 Marks |
| **TC5** | Blob Container access policy (Private container / no public access)             | 4 Marks |
| **TC6** | Secure transfer configuration (HTTPS-only traffic enforced)                     | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The storage account name must follow Azure naming rules (alphanumeric only, max 24 chars).
