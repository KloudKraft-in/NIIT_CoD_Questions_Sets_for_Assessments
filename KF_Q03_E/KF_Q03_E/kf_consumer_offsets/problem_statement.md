# Kafka Lab : Kafka Consumer Offsets Check

Duration : 60 Min.

## Scenario

Inspect partition offset progress to analyze backlog latency.

## Input Details

The environment has been pre-configured with the following resources:
- **Kafka Broker:** Pre-configured on localhost:9092

## Username & Naming Conventions

Your candidate prefix is a combination of your username (the part of your email/login before the `@` or `_` symbol) and exam code.
For example, if your username is `student` (or `student_niit.com`) and your exam code is `exam123`, your prefix is **`student-exam123`**.

You must name your resources accordingly:

- **Consumer Group:** `alerts-group-<prefix>` (e.g. `alerts-group-student-exam123`)

## Task Objectives

### 1. Track Consumer Group Offsets
- Consume messages and commit offset progress to the topic.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the environment.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Consumer group check (`alerts-group-<prefix>`) | 4 Marks |
| **TC2** | Commit offset verification | 4 Marks |
| **TC3** | Consumer connection check | 4 Marks |
| **TC4** | Reserved validation | 4 Marks |
| **TC5** | Reserved validation | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- Check that your script compiles cleanly and contains no syntax errors.
