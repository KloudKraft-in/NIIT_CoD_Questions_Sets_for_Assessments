import json
import os
import sys
import boto3
from datetime import datetime, timezone

# Capture Assessment Start Time
START_TIME_STR = os.getenv('NIIT_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else "LOCAL_USER"

def get_aws_clients():
    user_prefix = USER_PREFIX
    pipeline_name = f"labskraft-frontend-pipeline-{user_prefix}"
    
    aws_region = 'eu-west-2'
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_codepipeline = boto3.client('codepipeline', region_name=r)
            temp_codepipeline.get_pipeline(name=pipeline_name)
            aws_region = r
            break
        except Exception:
            try:
                temp_codecommit = boto3.client('codecommit', region_name=r)
                if temp_codecommit.list_repositories().get('repositories'):
                    aws_region = r
                    break
            except Exception:
                pass
                
    return boto3.client('s3'), boto3.client('codepipeline', region_name=aws_region), boto3.client('codecommit', region_name=aws_region)

def verify_task():
    user_prefix = USER_PREFIX
    start_time = START_TIME_STR
    
    # Standard LabsKraft Header
    print("\n" + "-"*70)
    print(f"{'NIIT REAL-TIME CI/CD AUDIT':^70}")
    print("-"*70)

    total_score = 0
    results = {}

    try:
        # Time Enforcement Logic
        if not START_TIME:
            print("[ERROR] NIIT_START_TIME environment variable is missing.")
            raise Exception("Invalid Session")

        now = datetime.now(timezone.utc)
        elapsed_minutes = (now - START_TIME).total_seconds() / 60
        max_duration = 75  # 75 Min assessment

        if elapsed_minutes > max_duration + 5: # 5 min grace
            print(f"[ERROR] Assessment duration exceeded. Elapsed: {elapsed_minutes:.1f}m / Allowed: {max_duration}m")
            raise Exception("Time Limit Exceeded")

        print(f"[SYSTEM] Validating Resources for: {user_prefix}")
        print(f"[SYSTEM] Session Active Time: {elapsed_minutes:.1f} mins\n")

        # Initialize Clients
        try:
            s3, codepipeline, codecommit = get_aws_clients()
        except Exception as e:
            print(f"[ERROR] Could not connect to AWS. Ensure credentials are set: {e}")
            raise e

        target_bucket = f"niit-web-app-{user_prefix}"
        pipeline_name = f"labskraft-frontend-pipeline-{user_prefix}"

        # --- TC1: Repository & S3 Hosting Setup ---
        tc1_passed = False
        valid_session = True
        try:
            # 1. Check if S3 bucket exists
            s3.head_bucket(Bucket=target_bucket)
            
            # Verify creation date if START_TIME is present
            if START_TIME:
                try:
                    buckets = s3.list_buckets().get('Buckets', [])
                    for b in buckets:
                        if b['Name'] == target_bucket:
                            b_date = b['CreationDate']
                            if b_date < START_TIME:
                                valid_session = False
                            break
                except Exception as e:
                    print(f"[WARN] Could not verify bucket creation date: {e}")
                    
            if not valid_session:
                raise Exception(f"Bucket '{target_bucket}' was created before the current assessment session started (Old Session).")
            
            # 2. Check if S3 Static website hosting is enabled
            website_configured = False
            try:
                web_config = s3.get_bucket_website(Bucket=target_bucket)
                if web_config:
                    website_configured = True
            except Exception:
                pass
            
            # 3. Check if repository is configured (any CodeCommit repo exists or pipeline connects to a repository)
            repo_configured = False
            try:
                repos = codecommit.list_repositories()
                if repos.get('repositories'):
                    repo_configured = True
            except Exception:
                pass
            
            # Fallback/Additional check: check if the pipeline has a Source action
            if not repo_configured:
                try:
                    pipe = codepipeline.get_pipeline(name=pipeline_name)
                    stages = pipe.get('pipeline', {}).get('stages', [])
                    for stage in stages:
                        if stage.get('name') == 'Source':
                            actions = stage.get('actions', [])
                            for action in actions:
                                act_type = action.get('actionTypeId', {})
                                if act_type.get('category') == 'Source':
                                    repo_configured = True
                                    break
                except Exception:
                    pass

            if repo_configured:
                tc1_passed = True
                results['tc1'] = True
                print(f"TC1: Repository Setup .................................. [PASSED] (2/2)")
            else:
                results['tc1'] = False
                print(f"TC1: Repository Setup .................................. [FAILED] (0/2)")
                print(f"     └─ [Reason]: Source repository (CodeCommit or GitHub) is not configured.")

            if website_configured:
                results['tc2'] = True
                print(f"TC2: S3 Hosting Setup .................................. [PASSED] (3/3)")
            else:
                results['tc2'] = False
                print(f"TC2: S3 Hosting Setup .................................. [FAILED] (0/3)")
                print(f"     └─ [Reason]: S3 bucket website hosting is not enabled.")
        except Exception as e:
            results['tc1'] = False
            results['tc2'] = False
            print(f"TC1: Repository Setup .................................. [FAILED] (0/2)")
            print(f"TC2: S3 Hosting Setup .................................. [FAILED] (0/3)")
            print(f"     └─ [Error]: {str(e)}")

        # --- TC3: AWS CodePipeline Configuration ---
        if not results.get('tc1') and not results.get('tc2'):
            results['tc3'] = False
            print(f"TC3: AWS CodePipeline Configuration .................... [FAILED] (0/2)")
            print(f"     └─ [Reason]: Prerequisite failed (TC1/TC2 invalid).")
            results['tc4'] = False
            print(f"TC4: Pipeline Execution & Deployment ................... [FAILED] (0/3)")
            print(f"     └─ [Reason]: Prerequisite failed.")
        else:
            try:
                # Get pipeline details
                pipe = codepipeline.get_pipeline(name=pipeline_name)
                stages = pipe.get('pipeline', {}).get('stages', [])
                
                has_source = False
                has_s3_deploy = False
                extract_enabled = False
                correct_bucket = False

                for stage in stages:
                    stage_name = stage.get('name')
                    actions = stage.get('actions', [])
                    for action in actions:
                        act_type = action.get('actionTypeId', {})
                        config = action.get('configuration', {})
                        
                        if stage_name == 'Source' or act_type.get('category') == 'Source':
                            has_source = True
                        
                        if stage_name == 'Deploy' or act_type.get('category') == 'Deploy':
                            if act_type.get('provider') == 'S3':
                                has_s3_deploy = True
                                if config.get('BucketName') == target_bucket:
                                    correct_bucket = True
                                if str(config.get('Extract')).lower() == 'true':
                                    extract_enabled = True

                if has_source and has_s3_deploy and correct_bucket and extract_enabled:
                    results['tc3'] = True
                    print(f"TC3: AWS CodePipeline Configuration .................... [PASSED] (2/2)")
                else:
                    reasons = []
                    if not has_source:
                        reasons.append("Source stage missing")
                    if not has_s3_deploy:
                        reasons.append("S3 Deploy stage missing")
                    elif not correct_bucket:
                        reasons.append(f"Deploy stage does not target the correct bucket '{target_bucket}'")
                    elif not extract_enabled:
                        reasons.append("Extract configuration 'Extract file before deploy' is not set to true")
                    results['tc3'] = False
                    print(f"TC3: AWS CodePipeline Configuration .................... [FAILED] (0/2)")
                    print(f"     └─ [Reason]: {', '.join(reasons)}.")
            except Exception as e:
                results['tc3'] = False
                print(f"TC3: AWS CodePipeline Configuration .................... [FAILED] (0/2)")
                print(f"     └─ [Error]: {str(e)}")
            
            # --- TC4: Pipeline Execution & Deployment ---
            try:
                # 1. Verify index.html exists in S3 bucket
                index_exists = False
                try:
                    s3.head_object(Bucket=target_bucket, Key='index.html')
                    index_exists = True
                except Exception:
                    pass

                # 2. Verify that CodePipeline execution was successful
                pipeline_succeeded = False
                try:
                    executions = codepipeline.list_pipeline_executions(pipelineName=pipeline_name)
                    exec_summaries = executions.get('pipelineExecutionSummaries', [])
                    if exec_summaries:
                        latest = exec_summaries[0]
                        if latest.get('status') == 'Succeeded':
                            pipeline_succeeded = True
                except Exception:
                    pass

                if index_exists and pipeline_succeeded:
                    results['tc4'] = True
                    print(f"TC4: Pipeline Execution & Deployment ................... [PASSED] (3/3)")
                else:
                    reasons = []
                    if not index_exists:
                        reasons.append(f"index.html not found in S3 bucket '{target_bucket}'")
                    if not pipeline_succeeded:
                        reasons.append("No successful pipeline execution found")
                    results['tc4'] = False
                    print(f"TC4: Pipeline Execution & Deployment ................... [FAILED] (0/3)")
                    print(f"     └─ [Reason]: {', '.join(reasons)}.")
            except Exception as e:
                results['tc4'] = False
                print(f"TC4: Pipeline Execution & Deployment ................... [FAILED] (0/3)")
                print(f"     └─ [Error]: {str(e)}")

        # Final Scoring
        total_score = 0
        if results.get('tc1'): total_score += 2
        if results.get('tc2'): total_score += 3
        if results.get('tc3'): total_score += 2
        if results.get('tc4'): total_score += 3
        
        print("-" * 70)
        print(f"{'TOTAL SCORE:':<52} {total_score}/10")
        print("-" * 70 + "\n")

    except Exception as e:
        print(f"[ERROR] Real-time audit failed: {str(e)}")
        total_score = 0

    # Save Metadata for Central Evaluation
    solution_data = {
        'candidate_prefix': user_prefix,
        'assessment_start_time': start_time,
        'evaluation_type': 'REAL_TIME_API',
        'score': total_score,
        'results': results
    }
    
    try:
        ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'student_workspace'))
        os.makedirs(ws_path, exist_ok=True)
        with open(os.path.join(ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
            
        root_ws_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_ws_path, 'solution.json'), 'w') as f:
            json.dump(solution_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not write solution.json: {e}")

if __name__ == '__main__':
    verify_task()
