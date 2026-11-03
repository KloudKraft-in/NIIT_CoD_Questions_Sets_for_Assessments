# Java Lab: Graceful Shutdown & Kubernetes PreStop Hooks

Duration : 60 Min.

## Scenario
Configure a Spring Boot application and a Kubernetes lifecycle pre-stop hook to execute graceful connection draining.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Locate `src/main/resources/application.properties`.
2. Configure graceful shutdown and termination timeout properties:
   `server.shutdown=graceful`
   `spring.lifecycle.timeout-per-shutdown-phase=30s`
3. Edit `pre-stop.sh` in the root workspace directory. Add a curl trigger command to wait/sleep for `10` seconds during container termination:
   `sleep 10`

## Verification
Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1   | server.shutdown=graceful set | 2 Marks |
| **TC2   | spring.lifecycle.timeout-per-shutdown-phase configured | 2 Marks |
| **TC3   | PreStop script path matches | 2 Marks |
| **TC4   | PreStop script sleep interval matches | 2 Marks |
| **TC5   | Properties syntax valid | 3 Marks |
| **TC6   | Active graceful shutdown settings loaded | 3 Marks |
| **TC7   | Starvation termination hooks active | 3 Marks |
| **TC8   | PreStop lifecycle delay active | 3 Marks |

**Total Score: 20 Marks**
