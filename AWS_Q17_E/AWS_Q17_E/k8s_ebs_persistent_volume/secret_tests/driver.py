import sys, os, subprocess, json

def run_cmd(cmd):
    try: return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
    except: return ""

def verify_task():
    print("-" * 40); print("KUBERNETES RESOURCE VERIFICATION REPORT"); print("-" * 40)
    sc_json = run_cmd("kubectl get sc -o json")
    pvc_json = run_cmd("kubectl get pvc -o json")
    deploy_json = run_cmd("kubectl get deployment nginx-app -o json")
    
    if '"ebs.csi.aws.com"' in sc_json or '"kubernetes.io/aws-ebs"' in sc_json or 'ebs-sc' in sc_json: print("TC1 [StorageClass] (2/2) - Success: Verified.")
    else: print("TC1 [StorageClass] (0/2) - Failed.")
        
    try:
        pvc = json.loads(pvc_json)
        found_pvc = False; is_bound = False; is_2gi = False
        for i in pvc.get('items', []):
            if i['metadata']['name'] == 'data-pvc':
                found_pvc = True
                if i['status']['phase'] == 'Bound': is_bound = True
                if i['spec']['resources']['requests'].get('storage') == '2Gi': is_2gi = True
                break
        
        if found_pvc: print("TC2 [PVC Exists] (1/1) - Success: Verified.")
        else: print("TC2 [PVC Exists] (0/1) - Failed.")
            
        if is_bound: print("TC3 [PVC Bound] (2/2) - Success: Verified.")
        else: print("TC3 [PVC Bound] (0/2) - Failed.")
            
        if is_2gi: print("TC5 [Storage 2Gi] (1/1) - Success: Verified.")
        else: print("TC5 [Storage 2Gi] (0/1) - Failed.")
    except:
        print("TC2 [PVC Exists] (0/1) - Failed.")
        print("TC3 [PVC Bound] (0/2) - Failed.")
        print("TC5 [Storage 2Gi] (0/1) - Failed.")

    try:
        d = json.loads(deploy_json)
        if d.get('status', {}).get('readyReplicas', 0) >= 1: print("TC4 [Deployment Running] (2/2) - Success: Verified.")
        else: print("TC4 [Deployment Running] (0/2) - Failed.")
            
        mounted = False
        for c in d.get('spec', {}).get('template', {}).get('spec', {}).get('containers', []):
            for vm in c.get('volumeMounts', []):
                if vm.get('mountPath') == '/usr/share/nginx/html': mounted = True
        if mounted: print("TC6 [Volume Mounted] (2/2) - Success: Verified.")
        else: print("TC6 [Volume Mounted] (0/2) - Failed.")
    except:
        print("TC4 [Deployment Running] (0/2) - Failed.")
        print("TC6 [Volume Mounted] (0/2) - Failed.")
    print("-" * 40)

if __name__ == "__main__":
    verify_task()
