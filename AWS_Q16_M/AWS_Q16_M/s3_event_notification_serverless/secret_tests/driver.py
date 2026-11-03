import sys, os, boto3, json

def verify_task():
    username = os.getenv('NIIT_USERNAME', 'LOCAL_USER')
    bucket_name = f"compliance-docs-{username}"
    topic_name = f"compliance-alerts-{username}"
    print("-" * 40); print("AWS RESOURCE VERIFICATION REPORT"); print("-" * 40)
    
    aws_region = 'eu-west-2'
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
        try:
            temp_sns = boto3.client('sns', region_name=r)
            topics = temp_sns.list_topics()['Topics']
            for t in topics:
                if topic_name in t['TopicArn']:
                    aws_region = r
                    break
            if aws_region == r:
                break
        except Exception:
            pass

    try:
        s3 = boto3.client('s3')
        sns = boto3.client('sns', region_name=aws_region)
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}"); return

    try:
        s3.head_bucket(Bucket=bucket_name)
        print("TC1 [Bucket Exists] (4/4) - Success: Verified.")
    except: print("TC1 [Bucket Exists] (0/4) - Failed.")

    topic_arn = None
    try:
        topics = sns.list_topics()['Topics']
        for t in topics:
            if topic_name in t['TopicArn']: topic_arn = t['TopicArn']; break
        if topic_arn:
            print("TC2 [Topic Exists] (3/3) - Success: Verified.")
            subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)['Subscriptions']
            if any(s['Protocol'] == 'email' for s in subs): print("TC3 [Email Subscription] (3/3) - Success: Verified.")
            else: print("TC3 [Email Subscription] (0/3) - Failed.")
                
            attrs = sns.get_topic_attributes(TopicArn=topic_arn)['Attributes']
            policy = attrs.get('Policy', '')
            if 's3.amazonaws.com' in policy and bucket_name in policy: print("TC4 [Topic Policy] (4/4) - Success: Verified.")
            else: print("TC4 [Topic Policy] (0/4) - Failed.")
        else: raise Exception("Not found")
    except:
        print("TC2 [Topic Exists] (0/3) - Failed.")
        print("TC3 [Email Subscription] (0/3) - Failed.")
        print("TC4 [Topic Policy] (0/4) - Failed.")

    try:
        notif = s3.get_bucket_notification_configuration(Bucket=bucket_name)
        tc = notif.get('TopicConfigurations', [])
        if tc and tc[0].get('TopicArn'):
            print("TC5 [S3 Event Configured] (3/3) - Success: Verified.")
            events = tc[0].get('Events', [])
            if any('ObjectCreated' in e for e in events): print("TC6 [S3 Event Filter] (3/3) - Success: Verified.")
            else: print("TC6 [S3 Event Filter] (0/3) - Failed.")
        else:
            print("TC5 [S3 Event Configured] (0/3) - Failed.")
            print("TC6 [S3 Event Filter] (0/3) - Failed.")
    except:
        print("TC5 [S3 Event Configured] (0/3) - Failed.")
        print("TC6 [S3 Event Filter] (0/3) - Failed.")
        
    print("-" * 40)

if __name__ == "__main__":
    verify_task()
