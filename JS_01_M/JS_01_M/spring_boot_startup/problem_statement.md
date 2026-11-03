# Java Lab: Resolve Spring Boot Startup Failures

Duration : 60 Min.

## Scenario
Diagnose and resolve startup failures in a Spring Boot application caused by port conflicts and bean wiring errors. You are provided with a standard Spring Boot web application. However, when you attempt to start the application, it crashes immediately due to two distinct configuration and code issues:
1. The application attempts to bind to the default port `8080`, which is restricted or occupied in this environment.
2. The application fails with a `NoSuchBeanDefinitionException` because a service dependency could not be found by the Spring container during startup.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Modify the code to resolve the Spring Bean wiring error (Hint: Check the `UserService` class).
- Modify the application configuration to change the server port to `8081`.
- Ensure the application compiles without errors.
- Start the application in the background (e.g., `mvn spring-boot:run &`).
- Ensure the application stays running and the `/actuator/health` endpoint returns a `200 OK` status.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives (e.g., `src/main/java/...`).
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands (like `mvn clean`), open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | Codebase compiles successfully | 4 Marks |
| **TC2** | The missing Spring Stereotype annotation is correctly added | 4 Marks |
| **TC3** | `application.properties` is configured to use port `8081` | 4 Marks |
| **TC4** | The Java application starts and remains running in the background | 4 Marks |
| **TC5** | The `/actuator/health` endpoint is accessible on port `8081` | 4 Marks |

**Total Score: 20 Marks**
