# Azure Lab: Azure Virtual Machine & Security Configuration (with Azure Bastion)

Duration : 45 Min.

## Scenario

As a DevOps Engineer at LabsKraft, you are tasked with provisioning a secure hosting environment in Microsoft Azure. Your objective is to deploy an Ubuntu virtual machine, configure network settings with appropriate security rules using a Network Security Group (NSG), set up a dedicated Azure Bastion subnet and Bastion host for secure administration, and verify that the virtual machine is deployed, configured, and actively running.

## Input Details

The environment has been pre-configured with the following resources:

- **Subscription:** LabsKraft
- **Resource Group:** `rg-iRUN-LTM-Assessment`
- **Region:** Asia Pacific East Asia (use `eastasia` region)

## Username & Naming Conventions

Your candidate prefix is the part of your Azure login email before the `@` symbol.
For example, if your Azure username is `ltmdemo01@michaelkloudkrafthotmail.onmicrosoft.com`, your prefix is **`ltmdemo01`**.

You must name your resources accordingly:

- **Virtual Network Name:** `vnet-<prefix>` (e.g. `vnet-ltmdemo01`)
- **Network Security Group Name:** `nsg-<prefix>` (e.g. `nsg-ltmdemo01`)
- **Bastion Host Name:** `bastion-<prefix>` (e.g. `bastion-ltmdemo01`)
- **Virtual Machine Name:** `vm-<prefix>` (e.g. `vm-ltmdemo01`)

## Task Objectives

Perform the following configuration steps directly in the Azure Portal or using the Azure CLI:

### 1. Configure Networking

- **Virtual Network Name:** `vnet-<prefix>`
- **Resource Group:** Use the pre-existing Resource Group `rg-iRUN-LTM-Assessment`.
- **Location:** Deploy the VNet in the `eastasia` region.
- **Address Space:** `10.0.0.0/16`
- **Subnets:**
  - Create a subnet named `default` (Subnet address range: `10.0.0.0/24`)
  - Create a subnet named `AzureBastionSubnet` (Subnet address range: `10.0.1.0/26`). *Note: The name must be exactly AzureBastionSubnet.*

### 2. Network Security Configuration

- **Network Security Group Name:** `nsg-<prefix>`
- **SSH Rule:** Create an inbound security rule to allow SSH traffic:
  - **Protocol:** TCP
  - **Destination Port Ranges:** `22`
  - **Source:** Any (`*`)
  - **Action:** Allow

### 3. Deploy Azure Bastion Host

- **Name:** `bastion-<prefix>`
- **Virtual Network:** `vnet-<prefix>`
- **Subnet:** `AzureBastionSubnet`
- **Public IP SKU:** Standard Public IP (Name: `bastion-ip`)

### 4. Deploy Virtual Machine

- **Virtual Machine Name:** `vm-<prefix>`
- **Size:** `Standard_B1s`
- **Operating System:** Ubuntu Server 22.04 LTS
- **Authentication:** Password or SSH Public Key (SSH Keys are recommended, but Password authentication is permitted)
- **Network Association:** Associate the VM's network interface with `vnet-<prefix>`, subnet `default`, and bind it to the Network Security Group `nsg-<prefix>`. The VM must be in a running state.
- **Connect using Bastion:** Connect to the VM using the Azure Bastion service directly from the browser portal.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Azure cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                                          | Marks   |
| ------------- | ---------------------------------------------------------------------------------------------------- | ------- |
| **TC1** | Resource Group validation (`rg-iRUN-LTM-Assessment` exists and is accessible)                      | 0 Marks |
| **TC2** | Virtual Network (`vnet-<prefix>` 10.0.0.0/16) and subnets default (`10.0.0.0/24`) & AzureBastionSubnet (`10.0.1.0/26`) | 4 Marks |
| **TC3** | NSG (`nsg-<prefix>`) exists and is associated                                                      | 4 Marks |
| **TC4** | NSG rules check (Inbound SSH traffic allowed on Port 22)                                             | 4 Marks |
| **TC5** | VM Bastion deployment validation (VM is running and connected to VNet, Bastion is associated with Standard SKU Public IP) | 4 Marks |
| **TC6** | VM Authentication Security (Authentication method is properly configured)                           | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The VM and Bastion host must be actively running during evaluation.

