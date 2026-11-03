# Java Lab: Maven Artefacts (JAR to WAR Conversion)

Duration : 60 Min.

## Scenario
Identify Maven build artefacts and successfully alter the deployment format from a standalone `jar` to a deployable `war` archive. You have a standard Spring Boot application configured to build as an executable `jar` file with an embedded Tomcat server. The infrastructure team has requested that this application be deployed to an external, standalone Tomcat application server. To achieve this, you must modify the `pom.xml` file to build a `.war` file instead of a `.jar` file, and ensure that the embedded Tomcat dependencies do not interfere with the external server.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Open the `pom.xml` file.
- Change the packaging type of the Maven project to `war`.
- Add the `spring-boot-starter-tomcat` dependency, but specifically mark its scope as `provided` so it is not bundled inside the final `.war` file.
- Run `mvn clean package` to build the project.
- Verify that a valid `.war` file is generated in the `target/` directory.

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
| **TC1** | `<packaging>war</packaging>` is correctly set in `pom.xml` | 4 Marks |
| **TC2** | The `spring-boot-starter-tomcat` dependency is added with `<scope>provided</scope>` | 4 Marks |
| **TC3** | `mvn clean package` executes successfully without compilation errors | 4 Marks |
| **TC4** | A `.war` file is successfully generated in the `target/` directory | 4 Marks |
| **TC5** | The generated `.war` file is a valid archive | 4 Marks |

**Total Score: 20 Marks**
