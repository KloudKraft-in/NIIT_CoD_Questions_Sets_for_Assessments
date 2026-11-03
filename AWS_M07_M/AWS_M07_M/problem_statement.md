# AWS Lab: High-Performance EBS Latency Spike & IOPS Burst Balance Triage

Duration : 90 Min.

## Scenario
An enterprise database running on an EC2 instance with a 200 GB gp2 EBS volume experiences severe query stalls every day at 14:00. CloudWatch metrics show that the volume's 'BurstBalance' metric drops from 100% to 0% after 45 minutes of heavy writes, collapsing disk performance from 3,000 IOPS down to the baseline 600 IOPS (3 IOPS per GB). Concurrently, VolumeQueueLength spikes to 48. The storage engineer must analyze the performance collapse, migrate the volume from legacy gp2 to gp3 with provisioned 12,000 IOPS and 500 MB/s throughput, and prove that burst depletion is eliminated.

## Input Details
The cloud environment has been pre-configured with the following parameters:
- **Platform:** Amazon EBS High Performance Storage & CloudWatch
- **Volume Configuration:** 200 GB legacy `gp2` (collapsed from 3,000 IOPS to 600 IOPS baseline)
- **Target Migration:** `gp3` with provisioned 12,000 IOPS and 500 MB/s throughput
- **Metric Collapse:** `BurstBalance` depleted to 0%, `VolumeQueueLength` spiked > 40

## Username & Naming Conventions
Your candidate prefix is: **`<prefix>`** (derived from your login email before the `@` symbol, e.g. `student-demo01`).
All custom resources and cloud configurations should incorporate this convention:
- **Resource Naming:** Prepend or append `<prefix>` to your created AWS resources (e.g. `<prefix>-resource`).
- **Candidate Tag:** Add tag `CandidatePrefix` = `<prefix>` on all managed cloud resources.

## Task Objectives
Perform the following technical objectives directly in the AWS Management Console or using the AWS CLI:
1. Ingest CloudWatch EBS metrics from /opt/aws_storage/ebs_burst_metrics.json.
2. Correlate BurstBalance depletion with spikes in VolumeTotalReadWriteTime and VolumeQueueLength.
3. Explain the mathematical mechanics of gp2 burst credits (accumulated I/O credits vs baseline consumption).
4. Formulate the AWS CLI command to modify the volume online: aws ec2 modify-volume --volume-id vol-0abc --volume-type gp3 --iops 12000 --throughput 500.
5. Verify that volume modification status transitions to 'optimizing' and then 'completed'.
6. Measure post-modification I/O latency under simulated load to confirm sub-5ms response time.
7. Author a comprehensive storage performance RCA report in ~/ebs_performance_rca.md.
8. Formulate an automated CloudWatch alarm to alert whenever VolumeQueueLength exceeds 10 for 5 minutes.

## Verification
Once completed, run the verification script to check your progress and receive your score. The verification system will inspect the live resources in the AWS cloud:
```bash
python run.py
```

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| :--- | :--- | :--- |
| **TC1** | Burst balance correlation: match BurstBalance drop to zero with the exact onset of database query timeouts | 3 Marks |
| **TC2** | Technical explanation: accurately explain gp2 3 IOPS/GB baseline limitation and burst bucket replenishment | 2 Marks |
| **TC3** | Queue depth analysis: interpret VolumeQueueLength > 40 as severe I/O bottleneck | 2 Marks |
| **TC4** | gp3 migration command: construct valid modify-volume command specifying gp3, 12000 IOPS, 500 MB/s | 3 Marks |
| **TC5** | Online optimization validation: verify volume status polling and zero downtime transition | 2 Marks |
| **TC6** | Performance benchmarking: post-upgrade latency metrics demonstrate sustained sub-5ms completion | 3 Marks |
| **TC7** | RCA report quality: ebs_performance_rca.md includes before/after graphs and financial ROI of gp3 vs gp2 | 3 Marks |
| **TC8** | Monitoring guardrail: CloudWatch alarm command correctly provisioned for proactive queue length alerting | 2 Marks |

**Total Score: 20 Marks**

## Important Notes
- Perform all actions directly in the AWS Management Console or using the AWS CLI.
- Ensure all resource configurations, tags, and naming conventions match the requirements.
- Do not terminate or alter pre-existing cloud infrastructure outside the scope of this assessment.
