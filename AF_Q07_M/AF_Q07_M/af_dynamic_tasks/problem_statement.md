# AF_Q07_M: Airflow Dynamic Task Mapping

## Scenario
The candidate must configure the following data operations setup in their workspace environment.

## Username & Naming Conventions
- Candidates must use their normalized username (`<username>`) and exam code (`<exam_code>`) for any resource creation.
- Default resources should follow prefix patterns like `<username>-<exam_code>`.

## Task Objectives
1. **Setup requirements**: Configure dynamic task expand mapping rules to parse variable file structures.
2. Ensure the resources pass standard structural and metadata checks.

## Verification
- Local run test script `run.py` can be executed to verify local workspace properties.
- Central validation runs queries against the live workspace to verify integration.

## Grading Criteria
- **TC1: Dynamic tasks compile check** (4 Marks)
- **TC2: Expand attributes confirm** (4 Marks)
- **TC3: Output mappings check** (4 Marks)
- **TC4: Parallel sequence verify** (4 Marks)
- **TC5: Status parsing logs** (4 Marks)

## Important Notes
- Always check that your syntax compiles without errors.
