# import sys
# import os
# import json
# from datetime import datetime, timezone, timedelta
# from azure.identity import ClientSecretCredential

# try:
#     from azure.mgmt.resource import ResourceManagementClient
# except ImportError:
#     try:
#         from azure.mgmt.resource.resources import ResourceManagementClient
#     except ImportError:
#         ResourceManagementClient = None

# try:
#     from azure.mgmt.storage import StorageManagementClient
# except ImportError:
#     try:
#         from azure.mgmt.storage.v2023_01_01 import StorageManagementClient
#     except ImportError:
#         StorageManagementClient = None


# # Capture Assessment Start Time
# START_TIME_STR = os.getenv('NIIT_START_TIME') or os.getenv('NIIT_START_TIME')
# START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
# USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', os.getenv('NIIT_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
# EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('NIIT_EXAM_CODE') or 'UNKNOWN')

# def verify_task():
#     print("-" * 65)
#     print(f"{'AZURE RESOURCE AUDIT (STORAGE)':^65}")
#     print("-" * 65)

#     total_score = 0
#     results = {
#         'tc1': False,
#         'tc2': False,
#         'tc3': False,
#         'tc4': False,
#         'tc5': False,
#         'tc6': False
#     }

#     try:
#         # Load Azure Credentials from the environment
#         subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
#         tenant_id = os.environ.get("AZURE_TENANT_ID")
#         client_id = os.environ.get("AZURE_CLIENT_ID")
#         client_secret = os.environ.get("AZURE_CLIENT_SECRET")

#         if not all([subscription_id, tenant_id, client_id, client_secret]):
#             print("TC1: Resource Group Access [FAILED] (0/0)")
#             print("     └─ [Reason]: Missing subscription_id, tenant_id, client_id, or client_secret.")
#             return

#         credential = ClientSecretCredential(
#             tenant_id=tenant_id,
#             client_id=client_id,
#             client_secret=client_secret
#         )

#         resource_client = ResourceManagementClient(credential, subscription_id)
#         storage_client = StorageManagementClient(credential, subscription_id)

#         # Resource configurations
#         azure_username = os.environ.get("AZURE_USERNAME")
#         if not azure_username:
#             azure_username = sys.argv[1] if len(sys.argv) > 1 else "default"
#         prefix = azure_username.split("@")[0].lower()
#         rg_name = "rg-iRUN-LTM-Assessment"
#         storage_account_name = f"store{prefix}".replace('-', '').replace('_', '')[:24]

#         # Print debug once
#         print(f"Azure Username: {azure_username}")
#         print(f"Azure Prefix: {prefix}")
#         print(f"Expected Storage Account: {storage_account_name}")
#         print(f"Expected Resource Group: {rg_name}")

#         # TC1: Resource Group validation (0 Marks)
#         tc1_passed = False
#         try:
#             resource_client.resource_groups.get(rg_name)
#             tc1_passed = True
#             print("TC1: Resource Group Access ............................ [PASSED] (0/0)")
#         except Exception as e:
#             print("TC1: Resource Group Access ............................ [FAILED] (0/0)")
#             print(f"     └─ [Reason]: Pre-created Resource Group '{rg_name}' not found. Details: {e}")
#             return

#         results['tc1'] = tc1_passed

#         # TC2: Storage Account existence in eastasia (4 Marks)
#         tc2_passed = False
#         sa = None
#         try:
#             sa = storage_client.storage_accounts.get_properties(rg_name, storage_account_name)
#             loc = sa.location.lower().replace(" ", "")
#             if loc == "eastasia":
#                 tc2_passed = True
#                 print("TC2: Storage Account Existence ........................ [PASSED] (4/4)")
#             else:
#                 print("TC2: Storage Account Existence ........................ [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Storage account is in '{sa.location}', expected 'eastasia'.")
#         except Exception as e:
#             print("TC2: Storage Account Existence ........................ [FAILED] (0/4)")
#             print(f"     └─ [Reason]: Storage account '{storage_account_name}' not found. Details: {str(e)}")

#         results['tc2'] = tc2_passed
#         if tc2_passed:
#             total_score += 4

#         # TC3: Storage Account SKU verification (4 Marks)
#         tc3_passed = False
#         if sa:
#             try:
#                 sku_name = sa.sku.name.value if sa.sku else ""
#                 if "Standard_LRS" in sku_name or "Standard" in sku_name:
#                     tc3_passed = True
#                     print("TC3: Storage Account SKU check ........................ [PASSED] (4/4)")
#                 else:
#                     print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
#                     print(f"     └─ [Reason]: Sku is expected to be Standard LRS, found '{sku_name}'.")
#             except Exception as e:
#                 print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Error checking SKU: {e}")
#         else:
#             print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite storage account not found.")

#         results['tc3'] = tc3_passed
#         if tc3_passed:
#             total_score += 4

#         # TC4: Blob Container existence (4 Marks)
#         tc4_passed = False
#         container = None
#         try:
#             container = storage_client.blob_containers.get(rg_name, storage_account_name, "assets")
#             tc4_passed = True
#             print("TC4: Blob Container Setup ............................. [PASSED] (4/4)")
#         except Exception as e:
#             print("TC4: Blob Container Setup ............................. [FAILED] (0/4)")
#             print(f"     └─ [Reason]: Blob container 'assets' not found under account '{storage_account_name}'. Details: {str(e)}")

#         results['tc4'] = tc4_passed
#         if tc4_passed:
#             total_score += 4

#         # TC5: Blob Container access policy (Private container / no public access) (4 Marks)
#         tc5_passed = False
#         if container:
#             try:
#                 public_access = container.public_access
#                 if public_access is None or str(public_access) == "PublicAccess.none":
#                     tc5_passed = True
#                     print("TC5: Container Public Access Policy ................... [PASSED] (4/4)")
#                 else:
#                     print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
#                     print(f"     └─ [Reason]: Container 'assets' public access level is '{public_access}', expected private.")
#             except Exception as e:
#                 print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Error checking access policy: {e}")
#         else:
#             print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite container not found.")

#         results['tc5'] = tc5_passed
#         if tc5_passed:
#             total_score += 4

#         # TC6: Secure transfer configuration (HTTPS-only traffic enforced) (4 Marks)
#         tc6_passed = False
#         if sa:
#             try:
#                 # check enable_https_traffic_only (secure transfer required)
#                 if sa.enable_https_traffic_only:
#                     tc6_passed = True
#                     print("TC6: Secure Transfer Enforcement ...................... [PASSED] (4/4)")
#                 else:
#                     print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
#                     print("     └─ [Reason]: 'Secure transfer required' (HTTPS only) is disabled.")
#             except Exception as e:
#                 print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
#                 print(f"     └─ [Reason]: Error checking HTTPS enforcement: {e}")
#         else:
#             print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
#             print("     └─ [Reason]: Prerequisite storage account not found.")

#         results['tc6'] = tc6_passed
#         if tc6_passed:
#             total_score += 4

#     except Exception as e:
#         print(f"[FATAL ERROR] Audit script crashed: {e}")

#     # Write test results for local agent evaluation parser
#     print(f"\n[SCORE] {total_score}")

# if __name__ == '__main__':
#     verify_task()

import sys
import os
import json
from datetime import datetime, timezone, timedelta
from azure.identity import ClientSecretCredential

try:
    from azure.mgmt.resource import ResourceManagementClient
except ImportError:
    try:
        from azure.mgmt.resource.resources import ResourceManagementClient
    except ImportError:
        ResourceManagementClient = None

try:
    from azure.mgmt.storage import StorageManagementClient
except ImportError:
    try:
        from azure.mgmt.storage.v2023_01_01 import StorageManagementClient
    except ImportError:
        StorageManagementClient = None


# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME') or os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NIIT_USERNAME', os.getenv('NIIT_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('NIIT_EXAM_CODE') or os.getenv('NIIT_EXAM_CODE') or 'UNKNOWN')

def verify_task():
    print("-" * 65)
    print(f"{'AZURE RESOURCE AUDIT (STORAGE)':^65}")
    print("-" * 65)

    total_score = 0
    results = {
        'tc1': False,
        'tc2': False,
        'tc3': False,
        'tc4': False,
        'tc5': False,
        'tc6': False
    }

    try:
        # Load Azure Credentials from the environment
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        tenant_id = os.environ.get("AZURE_TENANT_ID")
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")

        if not all([subscription_id, tenant_id, client_id, client_secret]):
            print("TC1: Resource Group Access [FAILED] (0/0)")
            print("     └─ [Reason]: Missing subscription_id, tenant_id, client_id, or client_secret.")
            return

        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        resource_client = ResourceManagementClient(credential, subscription_id)
        storage_client = StorageManagementClient(credential, subscription_id)

        # Resource configurations
        azure_username = os.environ.get("AZURE_USERNAME")
        if not azure_username:
            azure_username = sys.argv[1] if len(sys.argv) > 1 else "default"
        prefix = azure_username.split("@")[0].lower()
        rg_name = "rg-iRUN-LTM-Assessment"
        storage_account_name = f"store{prefix}".replace('-', '').replace('_', '')[:24]

        # Print debug once
        print(f"Azure Username: {azure_username}")
        print(f"Azure Prefix: {prefix}")
        print(f"Expected Storage Account: {storage_account_name}")
        print(f"Expected Resource Group: {rg_name}")

        # TC1: Resource Group validation (0 Marks)
        tc1_passed = False
        try:
            resource_client.resource_groups.get(rg_name)
            tc1_passed = True
            print("TC1: Resource Group Access ............................ [PASSED] (0/0)")
        except Exception as e:
            print("TC1: Resource Group Access ............................ [FAILED] (0/0)")
            print(f"     └─ [Reason]: Pre-created Resource Group '{rg_name}' not found. Details: {e}")
            return

        results['tc1'] = tc1_passed

        # TC2: Storage Account existence in eastasia (4 Marks)
        tc2_passed = False
        sa = None
        try:
            sa = storage_client.storage_accounts.get_properties(rg_name, storage_account_name)
            loc = sa.location.lower().replace(" ", "")
            if loc == "eastasia":
                # Validate creation time against START_TIME to prevent pre-creation
                creation_time = getattr(sa, 'creation_time', None)
                if START_TIME and creation_time:
                    # Ensure both are timezone aware
                    start_time = START_TIME
                    if creation_time.tzinfo is None:
                        creation_time = creation_time.replace(tzinfo=timezone.utc)
                    if start_time.tzinfo is None:
                        start_time = start_time.replace(tzinfo=timezone.utc)
                    
                    if creation_time < start_time:
                        tc2_passed = False
                        sa = None
                        print("TC2: Storage Account Existence ........................ [FAILED] (0/4)")
                        print("     └─ [Reason]: Storage account was found but not created in the current session.")
                    else:
                        tc2_passed = True
                        print("TC2: Storage Account Existence ........................ [PASSED] (4/4)")
                else:
                    tc2_passed = True
                    print("TC2: Storage Account Existence ........................ [PASSED] (4/4)")
            else:
                sa = None
                print("TC2: Storage Account Existence ........................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: Storage account is in '{sa.location}', expected 'eastasia'.")
        except Exception as e:
            sa = None
            print("TC2: Storage Account Existence ........................ [FAILED] (0/4)")
            print(f"     └─ [Reason]: Storage account '{storage_account_name}' not found. Details: {str(e)}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # TC3: Storage Account SKU verification (4 Marks)
        tc3_passed = False
        if tc2_passed and sa:
            try:
                sku_name = sa.sku.name.value if sa.sku else ""
                if "Standard_LRS" in sku_name or "Standard" in sku_name:
                    tc3_passed = True
                    print("TC3: Storage Account SKU check ........................ [PASSED] (4/4)")
                else:
                    print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
                    print(f"     └─ [Reason]: Sku is expected to be Standard LRS, found '{sku_name}'.")
            except Exception as e:
                print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: Error checking SKU: {e}")
        else:
            print("TC3: Storage Account SKU check ........................ [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite storage account not found or invalid.")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # TC4: Blob Container existence (4 Marks)
        tc4_passed = False
        container = None
        if tc2_passed:
            try:
                container = storage_client.blob_containers.get(rg_name, storage_account_name, "assets")
                
                # Check creation/last modified time of container to prevent pre-creation
                last_modified = getattr(container, 'last_modified_time', None)
                if START_TIME and last_modified:
                    start_time = START_TIME
                    if last_modified.tzinfo is None:
                        last_modified = last_modified.replace(tzinfo=timezone.utc)
                    if start_time.tzinfo is None:
                        start_time = start_time.replace(tzinfo=timezone.utc)
                        
                    if last_modified < start_time:
                        tc4_passed = False
                        container = None
                        print("TC4: Blob Container Setup ............................. [FAILED] (0/4)")
                        print("     └─ [Reason]: Blob container was found but not created in the current session.")
                    else:
                        tc4_passed = True
                        print("TC4: Blob Container Setup ............................. [PASSED] (4/4)")
                else:
                    tc4_passed = True
                    print("TC4: Blob Container Setup ............................. [PASSED] (4/4)")
            except Exception as e:
                print("TC4: Blob Container Setup ............................. [FAILED] (0/4)")
                print(f"     └─ [Reason]: Blob container 'assets' not found under account '{storage_account_name}'. Details: {str(e)}")
        else:
            print("TC4: Blob Container Setup ............................. [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite storage account not found or invalid.")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # TC5: Blob Container access policy (Private container / no public access) (4 Marks)
        tc5_passed = False
        if tc2_passed and tc4_passed and container:
            try:
                public_access = container.public_access
                public_access_str = str(public_access).lower() if public_access is not None else "none"
                if public_access is None or public_access_str in ["none", "publicaccess.none", "private"]:
                    tc5_passed = True
                    print("TC5: Container Public Access Policy ................... [PASSED] (4/4)")
                else:
                    print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
                    print(f"     └─ [Reason]: Container 'assets' public access level is '{public_access}', expected private.")
            except Exception as e:
                print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Error checking access policy: {e}")
        else:
            print("TC5: Container Public Access Policy ................... [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite container not found or invalid.")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # TC6: Secure transfer configuration (HTTPS-only traffic enforced) (4 Marks)
        tc6_passed = False
        if tc2_passed and sa:
            try:
                # check enable_https_traffic_only (secure transfer required)
                if sa.enable_https_traffic_only:
                    tc6_passed = True
                    print("TC6: Secure Transfer Enforcement ...................... [PASSED] (4/4)")
                else:
                    print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
                    print("     └─ [Reason]: 'Secure transfer required' (HTTPS only) is disabled.")
            except Exception as e:
                print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Error checking HTTPS enforcement: {e}")
        else:
            print("TC6: Secure Transfer Enforcement ...................... [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite storage account not found or invalid.")

        results['tc6'] = tc6_passed
        if tc6_passed:
            total_score += 4

    except Exception as e:
        print(f"[FATAL ERROR] Audit script crashed: {e}")

    # Write test results for local agent evaluation parser
    print(f"\n[SCORE] {total_score}")

if __name__ == '__main__':
    verify_task()
