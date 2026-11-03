import sys, os, boto3

def verify_task():
    username = os.getenv('NIIT_USERNAME', 'LOCAL_USER')
    repo_name = f"webapp-repo-{username}"
    print("-" * 40); print("AWS RESOURCE VERIFICATION REPORT"); print("-" * 40)
    aws_region = 'eu-west-2'
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_ecr = boto3.client('ecr', region_name=r)
            temp_ecr.describe_repositories(repositoryNames=[repo_name])
            aws_region = r
            break
        except Exception:
            pass

    try: ecr = boto3.client('ecr', region_name=aws_region)
    except Exception as e: print(f"FAILED: Could not connect to AWS. Error: {e}"); return
    
    try:
        repos = ecr.describe_repositories(repositoryNames=[repo_name])
        repo = repos['repositories'][0]
        print("TC1 [ECR Exists] (2/2) - Success: Verified.")
        
        if repo.get('imageTagMutability') == 'IMMUTABLE': print("TC2 [Mutability] (1/1) - Success: Verified.")
        else: print("TC2 [Mutability] (0/1) - Failed.")
            
        if repo.get('imageScanningConfiguration', {}).get('scanOnPush') == True: print("TC5 [Vulnerability Scan] (1/1) - Success: Verified.")
        else: print("TC5 [Vulnerability Scan] (0/1) - Failed.")
            
        imgs = ecr.describe_images(repositoryName=repo_name)['imageDetails']
        if len(imgs) > 0:
            print("TC3 [Image Exists] (2/2) - Success: Verified.")
            img = imgs[0]
            if len(img.get('imageTags', [])) > 0: print("TC4 [Image Tagged] (2/2) - Success: Verified.")
            else: print("TC4 [Image Tagged] (0/2) - Failed.")
                
            if img.get('imageManifestMediaType') or img.get('artifactMediaType'): print("TC6 [Architecture Valid] (2/2) - Success: Verified.")
            else: print("TC6 [Architecture Valid] (0/2) - Failed.")
        else:
            print("TC3 [Image Exists] (0/2) - Failed.")
            print("TC4 [Image Tagged] (0/2) - Failed.")
            print("TC6 [Architecture Valid] (0/2) - Failed.")
            
    except:
        print("TC1 [ECR Exists] (0/2) - Failed.")
        print("TC2 [Mutability] (0/1) - Failed.")
        print("TC3 [Image Exists] (0/2) - Failed.")
        print("TC4 [Image Tagged] (0/2) - Failed.")
        print("TC5 [Vulnerability Scan] (0/1) - Failed.")
        print("TC6 [Architecture Valid] (0/2) - Failed.")

    print("-" * 40)

if __name__ == "__main__":
    verify_task()
