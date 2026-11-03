# Kafka Lab : Kafka Topic Provisioning

Duration : 60 Min.

## Scenario

Configure new message queues on the Kafka broker.

## Input Details

The environment has been pre-configured with the following resources:
- **Kafka Broker:** Pre-configured on localhost:9092

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Topic Name:** `telemetry-stream-<prefix>` (e.g. `telemetry-stream-student-exam123`)

## Task Objectives

### 1. Create Topic
- Use kafka-topics tools to create the target queue.
- Define 3 partitions and a replication factor of 1.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Topic existence (`telemetry-stream-<prefix>` exists) | 4 Marks |
| **TC2** | Partition count check (3) | 4 Marks |
| **TC3** | Replication factor verification (1) | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
