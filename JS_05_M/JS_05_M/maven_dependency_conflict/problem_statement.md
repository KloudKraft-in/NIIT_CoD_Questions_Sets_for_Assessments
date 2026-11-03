# Java Lab: Resolve Classpath and Dependency Conflicts

Duration : 60 Min.

## Scenario
Identify and resolve classpath and dependency conflicts (Dependency Hell) in a Maven project. You are maintaining a Java application that uses Maven for dependency management. Recently, a developer added a new library, but the application now crashes at runtime (or compilation) due to a dependency conflict. Specifically, a transitive dependency is pulling in an outdated version of a library that clashes with a newer version explicitly required by the project. Your task is to analyze the dependency tree, identify the conflicting library, and use the `<exclusion>` tag in `pom.xml` to remove the outdated transitive dependency so the application compiles and runs successfully.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Run `mvn dependency:tree` to analyze the dependency structure.
- Identify which dependency is pulling in the conflicting transitive library.
- Open `pom.xml` and add an `<exclusion>` block to remove the conflicting dependency.
- Verify the conflict is resolved by running `mvn clean compile`.
- Ensure the application can start without a `NoSuchMethodError` or `ClassNotFoundException`.

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
| **TC1** | `pom.xml` has been modified by the student | 4 Marks |
| **TC2** | The `<exclusion>` tag is correctly applied for the conflicting library | 4 Marks |
| **TC3** | `mvn dependency:tree` confirms the conflicting version is removed | 4 Marks |
| **TC4** | Application compiles successfully (`mvn clean compile`) | 4 Marks |
| **TC5** | Application starts successfully (simulated by a clean run execution) | 4 Marks |

**Total Score: 20 Marks**
